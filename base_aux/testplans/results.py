# FIXME: THIS is an attempt to separate results!


from typing import *


# =====================================================================================================================
class TpResults:
    """
    Results for whole testplan at one dut!!!
    """
    TCS__CLS: dict[type['TC'], list['TC']]

    def __init__(self, tc: 'TC'):
        pass
        self.TC = tc
        # index will get from TC!!!

    @classmethod
    def set__tcs(cls, tcs):
        for tc in tcs:
            cls.TCS__CLS.update({tc: []})

    def clear(self, cls=None):
        pass

    def add_result(self, cls, result):
        pass

    def get_result(self, cls):
        pass


# =====================================================================================================================
