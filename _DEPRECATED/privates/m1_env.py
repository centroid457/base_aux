from typing import *
import os

from base_aux.privates.m0_base import *


# =====================================================================================================================
class PrivateEnv(PrivateBase):
    """
    read exact environs from Os Environment
    """
    def get_dict(self, _prefix: Optional[str] = None) -> TYPING.KWARGS_FINAL:
        """
        directly using result - mainly it is only for PRINTing and debugging! don't use result!

        NOTE: be careful to use result as dict! especially if you have lowercase letters!

        REASON:
            import os

            name_lowercase = "name_lowercase"
            os.environ[name_lowercase] = name_lowercase

            print(os.getenv(name_lowercase))    # name_lowercase
            print(os.getenv(name_lowercase.upper()))    # name_lowercase

            print(os.environ[name_lowercase])   # name_lowercase
            print(os.environ[name_lowercase.upper()])   # name_lowercase

            print(dict(os.environ)[name_lowercase])     # KeyError: 'name_lowercase'
        """
        envs_all = os.environ
        result: TYPING.KWARGS_FINAL = {}

        # filter ---------------
        for name, value in envs_all.items():
            if not _prefix or (_prefix and name.upper().startswith(_prefix.upper())):
                result.update({name: value})

        # print ---------------
        print()     # to pretty print in pytest only
        for name, value in result.items():
            print(f"{name}    ={value}")
        print()     # to pretty print in pytest only
        return result


# =====================================================================================================================
