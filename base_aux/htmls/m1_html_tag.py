from typing import *
from bs4 import BeautifulSoup
from base_aux.alerts.m2_select import *
from base_aux.alerts.m1_alert0_base import *
from base_aux.base_types.m2_info import *
from base_aux.chains.m1_chains import *


# =====================================================================================================================
# TODO: make tag access by attr name with calling and selection by kwargs
#   tag.a(**kwargs).header(**kwargs).b().a()


# =====================================================================================================================
class HtmlTagParser(NestCall_Resolve, NestInit_AnnotsAttr_ByKwargs):
    """
    GOAL
    ----
    get value(body/load) for exact html tag from source.
    if several tags found - return exact index!

    KWARGS - all params directly will be passed into function Tag.find_all!

    EXAMPLES
    --------
    HtmlTagAddress(name="table", attrs={"class": "donor-svetofor-restyle"}),
    """
    SOURCE: str = None
    INDEX: int = 0

    # BS4.find_all params ---------------------------------------------------------------------------------------------
    NAME: str = None
    ATTRS: dict[str, str] = dict()
    STRING: Optional[str] = None
    RECURSIVE: bool = None

    def __init__(self, source: str | BeautifulSoup = NoValue, **kwargs) -> None:
        if source not in [NoValue, None]:
            self.SOURCE = str(source)

        super().__init__(**kwargs)

    # -----------------------------------------------------------------------------------------------------------------
    def resolve(self, source: str | BeautifulSoup = NoValue) -> None | str:
        if source not in [NoValue, None]:
            self.SOURCE = str(source)

        return self.get_body()

    # -----------------------------------------------------------------------------------------------------------------
    def get_body(self) -> None | str:
        if self.SOURCE:
            try:
                bs_tag: BeautifulSoup = BeautifulSoup(markup=self.SOURCE, features='html.parser')
            except Exception as exx:
                msg = f"[CRITICAL] can't parse {self.SOURCE=}\n{exx!r}"
                Warn(msg)
                return
        else:
            msg = f"[CRITICAL] empty {self.SOURCE=}"
            Warn(msg)
            return

        # collect params ----------------------------------------------------------------------------------------------
        params = dict()
        if self.NAME is not None:
            params |= dict(name=self.NAME)
        if self.ATTRS:
            params |= dict(attrs=self.ATTRS)
        if self.STRING is not None:
            params |= dict(string=self.STRING)
        if self.RECURSIVE is not None:
            params |= dict(recursive=self.RECURSIVE)

        params |= dict(limit=self.INDEX + 1)

        # find --------------------------------------------------------------------------------------------------------
        try:
            tags = bs_tag.find_all(**params)
            bs_tag = tags[self.INDEX]
        except Exception as exx:
            msg = f"URL WAS CHANGED? can't find {self=}\n{exx!r}"
            Warn(msg)
            return

        return bs_tag.decode_contents()     # get exact internal boby(load) of tag without self-bracket-markup


# =====================================================================================================================
class ChainResolve_HtmlTagParser(ChainResolve):
    ON_RAISE: EnumAdj_ReturnOnRaise = EnumAdj_ReturnOnRaise.NONE


# =====================================================================================================================
def explore():
    load0 = 'hello<a href="http://example.com/">\nlink <i>example.com</i>\n</a>'

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

    # load = HtmlTagParser(load0, name="a").resolve()
    # print(f"{load=}")
    # load = HtmlTagParser(load0, name="i").resolve()
    # print(f"{load=}")

    print(f"{ChainResolve_HtmlTagParser(HtmlTagParser(name="a"), source=load0).resolve()=}")
    print(f"{ChainResolve_HtmlTagParser(HtmlTagParser(name="a")).resolve(source=load0)=}")
    print(f"{ChainResolve_HtmlTagParser(HtmlTagParser(name="a"), HtmlTagParser(name="i")).resolve(source=load0)=}")
    print(f"{ChainResolve_HtmlTagParser(HtmlTagParser(name="a"), HtmlTagParser(name="i"), source=load0).resolve()=}")


# =====================================================================================================================
if __name__ == "__main__":
    explore()
    # run_over_api()


# =====================================================================================================================
