# import time
import datetime


# =====================================================================================================================
class DateTime:
    TIMESTRUCT: datetime.datetime = None

    def __init__(self, timestruct = None):
        if timestruct is not None:
            self.TIMESTRUCT = timestruct

    def get_active__timestruct(self, value: datetime.datetime = None) -> datetime.datetime:
        # TODO: make get_first_valid from container!
        if value is None:
            value = self.TIMESTRUCT

        if value is None:
            value = datetime.datetime.now()

        return value

    def get_str(self, pattern: str = "%Y%m%d_%H%M%S", add_ms: bool = None, timestruct: datetime.datetime = None) -> str:
        """
        GOAL
        ----
        use for filenames like dumps/reservations/logs

        SPECIALLY CREATED FOR
        ---------------------

        EXAMPLES
        --------
        %Y%m%d_%H%M%S -> 20241203_114845
        add_ms -> 20241203_114934.805854
        """
        if add_ms:
            pattern += f".%f"

        timestruct = self.get_active__timestruct(timestruct)
        result = timestruct.strftime(pattern)
        return result

    def get_str__date(self, add_weekday: bool = None, pattern: str = "%Y.%m.%d", timestruct: datetime.datetime = None) -> str:
        """
        EXAMPLES
        --------
        %Y.%m.%d -> 2024.12.03.Tue
        """
        if add_weekday:
            pattern += ".%a"
        result = self.get_str(pattern=pattern, timestruct=timestruct)
        return result

    def get_str__time(self, add_ms: bool = None, pattern: str = "%H:%M:%S", timestruct: datetime.datetime = None) -> str:
        """

        EXAMPLES
        --------
        12:09:53
        12:11:53.855764
        """
        result = self.get_str(pattern=pattern, add_ms=add_ms, timestruct=timestruct)
        return result


# =====================================================================================================================
if __name__ == '__main__':
    print(DateTime().get_str__time(True))


# =====================================================================================================================
