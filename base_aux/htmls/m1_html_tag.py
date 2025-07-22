from typing import *
from bs4 import BeautifulSoup
from base_aux.alerts.m2_select import *
from base_aux.alerts.m1_alert0_base import *
from base_aux.base_types.m2_info import *


# =====================================================================================================================
class HtmlTagParser(NestCall_Resolve, Base_AttrKit):
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
    INDEX: int = 0

    # BS4.find_all ----------------------------------------------------------------------------------------------------
    # TODO: use as KWARGS???
    NAME: str = None
    ATTRS: dict[str, str] = dict()
    STRING: Optional[str] = None
    RECURSIVE: bool = None

    def __init__(self, source: str | BeautifulSoup = NoValue, **kwargs) -> None:
        if source is not NoValue:
            self.SOURCE = str(source)
        super().__init__(**kwargs)

    def resolve(self, source=NoValue, **kwargs) -> None | str:
        """
        GOAL
        ----
        from html source get load/body for exact tag
        """
        if source == NoValue:
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

        # collect params ---------
        params = dict()
        if self.NAME is not None:
            params |= dict(name=self.NAME)
        if self.ATTRS:
            params |= dict(attrs=self.ATTRS)
        if self.STRING is not None:
            params |= dict(string=self.STRING)
        if self.RECURSIVE is not None:
            params |= dict(string=self.RECURSIVE)

        params |= dict(limit=self.INDEX + 1)

        # find -------------------
        try:
            tags = bs_tag.find_all(**params)
            bs_tag = tags[self.INDEX]
        except Exception as exx:
            msg = f"URL WAS CHANGED? can't find {self=}\n{exx!r}"
            Warn(msg)
            return

        return bs_tag.decode_contents()     # get exact internal boby(load) of tag without self-bracket-markup


# =====================================================================================================================
# TODO: make tag access by attr name with calling and selection by kwargs
#   tag.a(**kwargs).header(**kwargs).b().a()


# =====================================================================================================================
def explore():
    load = 'hello<a href="http://example.com/">\nlink <i>example.com</i>\n</a>'

    # soup = BeautifulSoup(markup, 'html.parser')
    # print(soup.a)
    # print()
    # print()
    # print()
    # ObjectInfo(soup.a).print()
    #
    # print()
    # print()
    # print()

    # for name in dir(soup.a):
    #     print(name)

    load = HtmlTagParser(load, name="a").resolve()
    print(f"{load=}")
    load = HtmlTagParser(load, name="i").resolve()
    print(f"{load=}")


# =====================================================================================================================
if __name__ == "__main__":
    explore()
    # run_over_api()


# =====================================================================================================================
