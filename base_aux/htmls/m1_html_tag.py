from typing import *
import pathlib
import csv
import threading

import requests
from bs4 import BeautifulSoup

from base_aux.aux_eq.m3_eq_valid1_base import *

from base_aux.alerts.m2_select import *
from base_aux.alerts.m1_alert0_base import *


# =====================================================================================================================
class HtmlTagParser(NestInit_Source, NestCall_Resolve, Base_AttrKit):
    """
    GOAL
    ----
    create several chains to point to one tag.

    all params directly will be passed into function Tag.find_all!
    There is no variants - only full values!

    EXAMPLES
    --------
    HtmlTagAddress("table", {"class": "donor-svetofor-restyle"}),
    """
    SOURCE: str = None
    # CHAINS = ()

    # BS4.find_all -----------------------------
    NAME: str
    ATTRS: dict[str, str]
    TEXT_FIND: Optional[str] = None
    INDEX: int = 0

    def __init__(self, source: str | BeautifulSoup = None, **kwargs) -> None:
        if source is not None:
            self.SOURCE = str(source)

        super().__init__(**kwargs)

    def resolve(self, source=None, **kwargs) -> None | str:
        if source is None:
            source = self.SOURCE

        if source:
            try:
                bs_tag: BeautifulSoup = BeautifulSoup(markup=source, features='html.parser')
            except Exception as exx:
                msg = f"[CRITICAL] can't parse {source=}\n{exx!r}"
                Warn(msg)
                return
        else:
            msg = f"[CRITICAL] empty {source=}"
            Warn(msg)
            return

        try:
            tags = bs_tag.find_all(name=self.NAME, attrs=self.ATTRS, string=self.TEXT_FIND, limit=self.INDEX + 1)
            bs_tag = tags[self.INDEX]
        except Exception as exx:
            msg = f"URL WAS CHANGED? can't find {self=}\n{exx!r}"
            Warn(msg)
            return

        return str(bs_tag).strip()   # full markup!


# =====================================================================================================================
