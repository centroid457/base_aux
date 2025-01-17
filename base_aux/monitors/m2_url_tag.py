import time
from typing import *
import pathlib
import csv
import threading

import requests
from bs4 import BeautifulSoup

from base_aux.alerts.m2_select import *
from base_aux.alerts.m0_base import *


# =====================================================================================================================
# TODO: separate ClsBASE! see Imap!


# =====================================================================================================================
class TagAddressChain(NamedTuple):
    """structure which used as one step of full chain for finding Tag.
    all this params directly will be passed into function Tag.find_all!
    There is no variants - only full values!

    Main goal - create several chains to point to one tag.

    :ivar NAME: tag name for finding
    :ivar ATTRS: dict with expected attr names and exact values
        {"class": "donor-svetofor-restyle"}
    :ivar TEXT: text in expected tag
        None - if not specified
    :ivar INDEX: in case of found several tags - get the exact index of them

    EXAMPLES
    --------
    see in monitor implementations
        TagAddressChain("table", {"class": "donor-svetofor-restyle"}, None, 0),
    """
    NAME: str
    ATTRS: dict[str, str]
    TEXT: Optional[str]
    INDEX: int


class Alert_MonitorUrlTag(AlertSelect.TELEGRAM_DEF):
    """Just created exact class for Alerts!
    """
    pass


# =====================================================================================================================
class MonitorUrlTag(threading.Thread):
    """base class for final monitors!
    monitoring on URL some value.
    if found new value - remember it and send mail alert!

    :ivar URL: monitoring url
    :ivar TIMEOUT_REQUEST: timeout in request for html data
    :ivar INTERVAL: monitoring interval
    :ivar TAG_CHAINS: full chain to find exact tag
    :ivar TAG_GET_ATTR: which text get from found tag,
        None - from tag context,
        stringValue - from exact attribute name
    :ivar ALERT: object which will send the alerts
    :ivar DIRPATH: path to directory where will be saved history values
    :ivar CSV_DELIMITER: delimeter for history csvFile

    :ivar _source_data: full html for url
    :ivar _tag_found_last_chain: temporary kept last found tag object by one Chain
    :ivar value_last: last extracted value, jast for ability to compare alert state
    :ivar value_prelast: prelast extracted value

    :ivar msg: message (may be accumulated through process)
    """
    # SETTINGS -------------------------------
    URL: str = None
    TIMEOUT_REQUEST: int = 10
    INTERVAL: int = 1 * 60 * 60
    TAG_CHAINS: list[TagAddressChain] = []
    TAG_GET_ATTR: Optional[str] = None
    ALERT: type[AlertBase] = Alert_MonitorUrlTag

    DIRPATH: pathlib.Path = pathlib.Path("USERDATA")
    CSV_DELIMITER: str = ";"

    # internal ----------------------------------
    _source_data: str = ""
    _tag_found_last_chain: Optional[BeautifulSoup] = None
    value_last: str = None
    value_prelast: str = None
    msg: str = ""

    def __init__(self):
        super().__init__(daemon=False)

        self.DIRPATH = pathlib.Path(self.DIRPATH)
        self.FILEPATH = self.DIRPATH.joinpath(f"{self.NAME}.csv")

        self.DIRPATH.mkdir(exist_ok=True)
        if self.FILEPATH.exists():
            self.value_last__load()
        else:
            self.FILEPATH.touch(exist_ok=True)

        self.start()

    @property
    def NAME(self):
        """class name
        """
        return self.__class__.__name__

    def value_last__load(self) -> None:
        """load last value from history
        """
        if not self.FILEPATH.exists():
            return

        with open(self.FILEPATH, "rt", newline='') as ofilepath:
            reader = csv.reader(ofilepath, delimiter=self.CSV_DELIMITER)
            result = None
            for line_parsed in reader:
                result = line_parsed[1]
            self.value_last = self.value_prelast = result

    def value_last__save(self) -> None:
        """save last value from history
        """
        with open(self.FILEPATH, "a", newline='') as ofilepath:
            writer = csv.writer(ofilepath, delimiter=self.CSV_DELIMITER)
            writer.writerow([time.strftime("%Y.%m.%d %H:%M:%S"), self.value_last])

    def run(self):
        """MAIN function working in thread
        """
        while True:
            if self.alert_state__check():
                self.ALERT(self.msg)

            print(self.msg)
            time.sleep(self.INTERVAL)

    def alert_state__check(self) -> bool:
        """check alert state

        :returns:
            True - if need ALERT!
            there is only one way to return False - all funcs get true(correctly finished) and oldValue == newValue.
            Otherwise, need send email!!!
            if some func get false or finished incorrect - we will have smth in self.msg!
        """
        result = True
        if all([
            self.reinit_values(),
            self.source__load(),
            self.source__get_tag(),
            self.tag__get_value(),
            ]):

            if self.value_last != self.value_prelast:
                self.msg += f"DETECTED CHANGE[{self.value_prelast}->{self.value_last}]"
                self.value_last__save()
            else:
                self.msg += f"SameState[{self.value_prelast}->{self.value_last}]"
                result = False

        return result

    def reinit_values(self) -> True:
        """clear main values on new monitor cycle
        """
        self.msg = ""
        self._source_data = ""
        self._tag_found_last_chain = None
        return True

    def source__load(self) -> bool:
        """load url source data
        """
        self._source_data = ""
        try:
            response = requests.get(self.URL, timeout=self.TIMEOUT_REQUEST)
            self._source_data = response.text
            return True
        except Exception as exx:
            self.msg += f"LOST URL {exx!r}"

    def source__get_tag(self) -> Optional[bool]:
        """find tag from source and save tag object in attribute
        """
        if self._source_data:
            try:
                self._tag_found_last_chain = BeautifulSoup(markup=self._source_data, features='html.parser')
            except Exception as exx:
                self.msg += f"[CRITICAL] can't parse {self._source_data=}\n{exx!r}"
                return
        else:
            self.msg += f"[CRITICAL] empty {self._source_data=}"
            return

        try:
            for chain in self.TAG_CHAINS:
                tags = self._tag_found_last_chain.find_all(name=chain.NAME, attrs=chain.ATTRS, string=chain.TEXT, limit=chain.INDEX + 1)
                self._tag_found_last_chain = tags[chain.INDEX]
        except Exception as exx:
            self.msg += f"URL WAS CHANGED! can't find {chain=}\n{exx!r}"
            return

        return True

    def tag__get_value(self) -> Optional[bool]:
        """get resulting value from found tag
        """
        if not self._tag_found_last_chain:
            return

        self.value_prelast = self.value_last

        if self.TAG_GET_ATTR is None:
            self.value_last = self._tag_found_last_chain.string
        else:
            self.value_last = self._tag_found_last_chain[self.TAG_GET_ATTR][0]

        if isinstance(self.value_last, str):
            self.value_last = self.value_last.strip()
        return True


# =====================================================================================================================
