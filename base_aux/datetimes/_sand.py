import time
import datetime


# =====================================================================================================================
class TimeoutWorker:   # starichenko
    # better use _LogProgressBar!
    def __init__(self, timeout=0):
        """
        :param timeout: if use 0 or None - used just like a stopwatch
        """
        self.time_start = time.time()
        self.timeout = timeout
        self._drop_flag = False

    def check_finish(self):
        return self._drop_flag or self.get_time_passed() > self.timeout

    def restart(self):
        self.time_start = time.time()
        self._drop_flag = False
        return True

    def wait_timeout(self, step=1, restart=False):
        """actually waiting whole timeout"""
        if restart:
            self.restart()
        while not self.check_finish():
            time.sleep(step)
        return True

    def drop(self):
        """stop timeout"""
        self._drop_flag = True
        return True

    # def get_time_passed(self, cutting_level=None):
    #     result = time.time() - self.time_start
    #     result = number_cutting(source=result, cutting_level=cutting_level)
    #     return result


def time_convert_to_human(seconds):
    # toDO: use standart python time formatting!
    try:
        if seconds <= 0:
            return ""
    except TypeError:
        raise Exception("Cannot convert '{}' to human time".format(seconds))

    human_time_string = ""
    days = seconds // 86400
    hours = seconds // 3600 % 24
    minutes = seconds // 60 % 60
    seconds = seconds % 60
    if days:
        human_time_string = human_time_string + str(days) + 'д.'
    if hours:
        human_time_string = human_time_string + str(hours) + 'ч.'
    if minutes:
        human_time_string = human_time_string + str(minutes) + 'м.'
    if seconds:
        human_time_string = human_time_string + str(seconds) + 'с.'

    return human_time_string


# def time_sleep_with_log(seconds=1, msg=None):   # starichenko
#     """ logging steps of pause sleep.
#     usefull when you want to be sure that process is going!
#     """
#     # debug_stack_get_list()
#     MSG_DEFAULT = f"WAIT seconds/step=[{seconds}]"
#     msg = msg or MSG_DEFAULT
#
#     seconds = float(seconds)
#     progress_obj = LogProgressBarTimeout(max_value=seconds, title=msg)
#
#     while not progress_obj.check_finish():
#         progress_obj.update()
#         time.sleep(1)
#
#     progress_obj.update_status(True)
#     return True


def time_get_offset_to_now(start):  # starichenko
    """return time offset from start in seconds to now!
    """
    return time.time() - start


def time_sleep_remaining_time(seconds=1, start=None):   # starichenko
    """sleep remaining time from start point!

    :param seconds: expected time for sleep from start point
    :param start: start point time in seconds
        if None - sleep all seconds time

    :return: deviation seconds
        if deviation less then zero - return it without sleeping with minus!
    """
    time_now = time.time()

    if start is None:
        time_remain = seconds
    else:
        time_past = time_now - start
        time_remain = seconds - time_past

        if time_remain > 0:
            time.sleep(time_remain)

    return time_remain


def time_get_in_full_seconds_from_structtime(source=None):   # starichenko
    """
    created specially to get time in seconds to compare volga localtime with system.
    :param source:
    :return:
    """
    source = source or time.time()
    seconds = source.tm_sec + source.tm_min*60 + source.tm_hour*60*60
    return seconds


# =====================================================================================================================
