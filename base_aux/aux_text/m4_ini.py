from typing import *
import configparser

from base_aux.aux_text.m1_text_aux import *
from base_aux.base_inits.m1_nest_init_source import *
from base_aux.base_statics.m1_types import *


# =====================================================================================================================
class ConfigParserMod(configparser.ConfigParser):
    """
    GOAL
    ----
    just add some dict-meths into original class
    """
    def to_dict__direct(self) -> TYPING.DICT_STR_STR:
        """
        NOTE
        ----
        it is just an ability!
        use final MERGED and KEEP SOURCE in CORRECT struct! NoDEFAULTS or know what you do!!
        """
        # use double places!
        result = dict(self._defaults)
        result.update({"DEFAULT": dict(self._defaults)})

        # sections
        result.update(dict(self._sections))
        return result

    def to_dict__merged(self) -> TYPING.DICT_STR_STR:
        result = self.to_dict__direct()
        for section in self.sections():
            for def_name, def_val in self._defaults.items():
                if def_name not in result[section]:
                    result[section][def_name] = def_val
        return result

    def to_dict(self) -> TYPING.DICT_STR_STR:
        return self.to_dict__merged()

    # -----------------------------------------------------------------------------------------------------------------
    def read_string(self, string: str, *args, **kwargs) -> None | NoReturn:
        """
        GOAL-mod
        ----
        just fix default section
        """
        try:
            super().read_string(string, *args, **kwargs)
        except:
            string = f"[DEFAULT]\n{string}"
            super().read_string(string, *args, **kwargs)


# =====================================================================================================================
def _explore():
    config = ConfigParserMod()
    config.set("DEFAULT", "name0", "000")
    config.add_section("SEC1")
    config.set("SEC1", "name1", "111")
    config.set("SEC1", "name2", "222")
    config.set("SEC1", "name3", "333")
    print(config.to_dict__direct())
    print(config.to_dict__merged())


# =====================================================================================================================
if __name__ == '__main__':
    _explore()


# =====================================================================================================================
