from base_aux.stock.m4_strategy import *


class MonitorADX(MonitorADX):
    THRESH_ADX_FAST_FULL = 80
    THRESH_ADX_SLOW_FULL = 50


def main():
    MonitorADX().join()
    # trade_alerts.IndicatorMapDrawer_Simple().join()


if __name__ == "__main__":
    main()
    