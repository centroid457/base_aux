import sys

from base_aux.aux_np_pd.m1_np import *
from base_aux.alerts.m2_select import *
from base_aux.base_lambdas.m4_thread_collector import *

from base_aux.stock.m1_mt import *


# =====================================================================================================================
pass    # settings
np.set_printoptions(threshold=sys.maxsize, linewidth=300)


# =====================================================================================================================
class MonitorBase(MT5, threading.Thread):
    """Base monitor class.

    :ivar ALERT: Alert class used instantiating send msg
    :ivar counter: count active monitoring steps
    :ivar state_calculating: state when step is in active calculating phase
        new bar get + calculatings started and not yet finished
    :ivar LOAD_HISTORY_BARS: apply calculations on exact history bars
    """
    ALERT: type[Base_Alert] = None
    counter: int = 0
    state_calculating: bool = None
    LOAD_HISTORY_BARS: int = 10

    def __init__(self):
        super().__init__()
        self.ALERT(f"start strategy")
        self.LOAD_HISTORY_BARS = self.LOAD_HISTORY_BARS or 0
        self.start()

    def run(self):
        """manage cycles of monitoring
        """
        while True:
            self.counter += 1
            self.state_calculating = True

            print()
            msg = f"[OK]cycle new [{self.counter=}]"
            print(msg)

            self.run_strategy_cycle_one()
            self.ALERT.wait()

            self.state_calculating = False

            if not self.LOAD_HISTORY_BARS:
                self.history_new__wait()
            else:
                self.LOAD_HISTORY_BARS -= 1

    def run_strategy_cycle_one(self):
        """Execute one full cycle
        """
        pass


# =====================================================================================================================
class AlertTradeADX(AlertSelect.TELEGRAM_DEF):
    """exact alert object for ADX Strategy
    """
    pass


class ThreadDeCollectorADX(ThreadsDecorCollector):
    """Manager which create new group of threads
    """
    pass


class MonitorADX(MonitorBase):
    TF = 1
    ALERT: type[Base_Alert] = AlertTradeADX

    # LOCAL --------------------------
    ADX_FAST: tuple[int, int] = (6, 2)
    ADX_SLOW: tuple[int, int] = (10, 7)

    PULSE_TAIL: int = 20
    THRESH_ADX_FAST_FULL: int = 80  # 80
    THRESH_ADX_SLOW_FULL: int = 50  # 50

    state_full_column_1_10: bool = None

    TF_SHIFTED_MAX: int = 120
    LOAD_HISTORY_BARS: int = 1
    RESULTS: np.ndarray = None

    ARRAY_INTERPRETER: dict[Literal[-1, 0, 1, 2], Any] = {
        -1: " ",    # not exists
        0: "_",     # exists and no Pulse
        # 1: "*",     # Pulse
        # 2: "#"      # edge pulse
        3: "#"      # edge pulse
    }

    def __init__(self):
        self.RESULTS = np.full(shape=(self.TF_SHIFTED_MAX, self.TF_SHIFTED_MAX), fill_value=-1, dtype=int)
        super().__init__()

    def run_strategy_cycle_one(self):
        for tf_shifted in range(1, self.TF_SHIFTED_MAX + 1):
            self.calculate__tf_shifted(tf_shifted)
        ThreadDeCollectorADX().wait_all()
        self.adx_full_pulse_1_10_check()
        self.print__array_interpreted()
        # self.ALERT("tf_shifted checked")

    def adx_full_pulse_1_10_check(self) -> None:
        results_10 = self.results_length_get(10)
        results_15 = self.results_length_get(15)
        counter = 0
        if (results_10 > 0).sum() or (results_15 > 0).sum():
            for tf_shifted in range(1, 10):
                if (self.results_length_get(tf_shifted) > 0).sum():
                    counter += 1

        if counter >= 8:
            if not self.state_full_column_1_10:
                self.state_full_column_1_10 = True
                self.ALERT(body=f"ADX FULL COLUMN!")
        else:
            self.state_full_column_1_10 = False

    def print__array_interpreted(self) -> None:
        text = NpAux(self.RESULTS).d2_get_compact_str(
            values_translater=self.ARRAY_INTERPRETER,
            separate_rows_blocks=20,
            wrap=True,
            use_rows_num=True
        )
        print()
        print(text)
        print()
        print()
        print()
        return

    @ThreadDeCollectorADX().decorator__to_thread
    def calculate__tf_shifted(self, tf_shifted: int) -> None:
        tf_shifted_index = tf_shifted - 1
        # DATA ----------------------------------------
        adx_fast = self.indicator_ADX(self.ADX_FAST, tf_split=tf_shifted, return_tail=self.PULSE_TAIL, _add_history=self.LOAD_HISTORY_BARS)
        adx_slow = self.indicator_ADX(self.ADX_SLOW, tf_split=tf_shifted, return_tail=self.PULSE_TAIL, _add_history=self.LOAD_HISTORY_BARS)

        adx_fast.reset_index(drop=True, inplace=True)
        adx_slow.reset_index(drop=True, inplace=True)

        adx_fast_slow = pd.concat([adx_fast, adx_slow], axis=1)

        # CHECKS ----------------------------------------
        # state-1=PULSE IN CURRENT STEP
        state_pulse__tf_shifted = self.check__state_pulse__tf_shifted(adx_fast, adx_slow)
        result__tf_shifted = int(state_pulse__tf_shifted)   # 0/1

        # state-2=FIRST PULSE IN CURRENT STEP
        state_pulse__tf_shifted_edge = self.check__state_pulse__tf_shifted_edge(adx_fast, adx_slow)
        if state_pulse__tf_shifted_edge:
            result__tf_shifted = 2

        self.RESULTS[tf_shifted_index] = np.roll(self.RESULTS[tf_shifted_index], -1)
        self.RESULTS[tf_shifted_index][-1] = result__tf_shifted

        # state-3=FIRST PULSE IN GROUP STEPS
        results_steps = self.results_length_get(tf_shifted)
        count_steps__existed = (results_steps >= 0).sum()
        count_steps__pulsed = (results_steps > 0).sum()

        state_pulse__group_edge = False
        if state_pulse__tf_shifted_edge:
            if count_steps__existed > 1:
                state_pulse__group_edge = count_steps__pulsed == 1
            elif count_steps__existed == 1:
                state_pulse__group_edge = True

        if state_pulse__group_edge:
            result__tf_shifted = 3
        self.RESULTS[tf_shifted_index][-1] = result__tf_shifted
        results_steps = self.RESULTS[tf_shifted_index][self.TF_SHIFTED_MAX - tf_shifted: self.TF_SHIFTED_MAX]

        if result__tf_shifted == 3 and not self.LOAD_HISTORY_BARS:
            msg = f"[m{self.TF}/sh={tf_shifted}]\n"
            msg += f"{adx_fast_slow}\n"
            msg += f"{list(results_steps)}\n"
            self.ALERT(body=msg)

    def results_length_get(self, length: int):
        return self.RESULTS[length - 1][self.TF_SHIFTED_MAX - length: self.TF_SHIFTED_MAX]

    def check__state_pulse__tf_shifted(self, adx_fast: TYPING__PD_SERIES, adx_slow: TYPING__PD_SERIES) -> bool:
        return np.max(adx_fast) >= self.THRESH_ADX_FAST_FULL and np.max(adx_slow) >= self.THRESH_ADX_SLOW_FULL

    def check__state_pulse__tf_shifted_edge(self, adx_fast: TYPING__PD_SERIES, adx_slow: TYPING__PD_SERIES) -> bool:
        if np.max(adx_fast) >= self.THRESH_ADX_FAST_FULL:
            if np.max(adx_slow.head(len(adx_slow) - 1)) < self.THRESH_ADX_SLOW_FULL <= adx_slow.iloc[len(adx_slow) - 1]:
                return True

        if np.max(adx_slow) >= self.THRESH_ADX_SLOW_FULL:
            if np.max(adx_fast.head(len(adx_fast) - 1)) < self.THRESH_ADX_FAST_FULL <= adx_fast.iloc[len(adx_fast) - 1]:
                return True

        return False


# =====================================================================================================================
pass     # ============================================================================================================
pass     # ============================================================================================================
pass     # ============================================================================================================
pass     # ============================================================================================================
pass     # ============================================================================================================


# =====================================================================================================================
class Alert_MapDrawer(AlertSelect.TELEGRAM_DEF):
    """exact alert object for ADX Strategy
    """
    pass


class ThreadDeCollector_MapDrawer_Tf(ThreadsDecorCollector):
    """Manager which create new group of threads
    """
    pass


class ThreadDeCollector_MapDrawer_Shift(ThreadsDecorCollector):
    """Manager which create new group of threads
    """
    pass


class IndicatorMapDrawer_Simple(MT5, threading.Thread):
    ALERT: type[Base_Alert] = Alert_MapDrawer
    INDICATOR: type[Base_IndicatorParams] = IndicatorParams_RSI
    INDICATOR_SETTINGS: Iterable[int] = (5, )

    TF = mt5.TIMEFRAME_D1

    MAP_LENGTH: int = 10    #100
    MAP_HEIGHT: int = 1    #10

    MAP: np.ndarray = None

    history: np.ndarray = None

    def __init__(self):
        super().__init__()
        self.ALERT(f"start strategy")
        self.start()

    def run(self):
        self.calculate_tfs()
        print()
        print(self.MAP)
        print()

    def calculate_tfs(self):
        """create exactly the MAP = all rows
        """

        # TODO: MOVE INTO MT5!!! in indicator!
        for tf_assembled in range(1, self.MAP_HEIGHT + 1):
            self.calculate_tf(tf_assembled)
        ThreadDeCollector_MapDrawer_Tf().wait_all()

    @ThreadDeCollector_MapDrawer_Tf().decorator__to_thread
    def calculate_tf(self, tf_split: int):
        """calculates all steps for exact TF - its just one row in MAP!
        """
        # define final count of bars
        count_need = self.INDICATOR(*self.INDICATOR_SETTINGS).bars_expected__get() + self.MAP_LENGTH

        # get history
        history = self.history__get(count=count_need, tf_multiply=tf_split)

        # add results
        for shift in range(tf_split):
            self.calculate_shift(shift, tf_split, history)
        ThreadDeCollector_MapDrawer_Shift().wait_all()

        # results = collect
        threads_sorted = sorted(ThreadDeCollector_MapDrawer_Shift().THREAD_ITEMS, key=lambda x: x.args[0])
        results: np.ndarray = np.array([thread.result for thread in threads_sorted])

        # results = flat
        result = results.flatten("F")

        # save row to MAP
        self.MAP[tf_split - 1] = result

    @ThreadDeCollector_MapDrawer_Shift().decorator__to_thread
    def calculate_shift(self, shift: int, tf_split: int, history: np.ndarray) -> np.ndarray:
        history = history[shift::tf_split]
        result = self._indicator_get_by_obj(self.INDICATOR(*self.INDICATOR_SETTINGS), _bars=history, return_tail=self.MAP_LENGTH//tf_split)
        print()
        print(result)
        print()
        return result


# =====================================================================================================================
