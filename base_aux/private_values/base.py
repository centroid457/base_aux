from typing import *
import pathlib
import abc

from base_aux.classes_aux import AnnotAux
from . import Exx__FileNotExists, TYPE__PATH


# =====================================================================================================================
# TODO: add iter???


# =====================================================================================================================
class PrivateBase(AnnotAux, abc.ABC):
    """Base class to get values from sources.

    :ivar SECTION: first level name in source, for ini - root section, for json - rootKey, for env - not used
    :ivar DIRPATH: file destination
    :ivar FILENAME: file name

    USAGE
    -----
    if you dont need RAISE when no value get for exact annotated name - just define None!
    """
    DONT_CHECK_VALUES_EXISTS: Optional[bool] = None

    SECTION: Optional[str] = None

    DIRPATH: Optional[TYPE__PATH] = pathlib.Path.home()
    FILENAME: Optional[str] = None

    _text: Optional[str] = None     # TODO: need tests!!!
    dict: Dict[str, Any] = None

    # -----------------------------------------------------------------------------------------------------------------
    def __init__(
            self,
            _section: Optional[str] = None,

            _dirpath: TYPE__PATH = None,
            _filename: str = None,
            _filepath: TYPE__PATH = None,

            _text: Optional[str] = None,                # instead of file
            _dict: Optional[Dict[str, Any]] = None,     # instead of file

            _dont_check_values_exists: Optional[bool] = None
    ):
        super().__init__()
        self.SECTION = _section or self.SECTION

        if _dict is not None:
            self.SECTION = None
            self.DIRPATH = None
            self.FILENAME = None
            self.apply_dict(_dict)
        elif _text is not None:
            self.DIRPATH = None
            self.FILENAME = None
            self._text = _text
        else:
            self._filepath_apply_new(
                _dirpath=_dirpath,
                _filename=_filename,
                _filepath=_filepath
            )

        if _dict is None:
            self.load_dict()

        if not _dont_check_values_exists:
            self.annot__raise_if_not_defined()

    def __str__(self):
        """return pretty string
        """
        result = f"{self.filepath=}"
        data = self.get_dict()
        if data:
            for key, value in data.items():
                result += f"\n{key}={value}"
        elif self.filepath and self.filepath.exists():
            result += f"\n{self._text}"
        else:
            result += f"\ndata=None"
        return result

    # -----------------------------------------------------------------------------------------------------------------
    def _filepath_apply_new(
            self,
            _dirpath: TYPE__PATH = None,
            _filename: str = None,
            _filepath: TYPE__PATH = None
    ) -> Optional[NoReturn]:
        """apply new file destination
        """
        if not _filepath:
            self.DIRPATH = pathlib.Path(_dirpath or self.DIRPATH)
            self.FILENAME = _filename or self.FILENAME
        else:
            self.DIRPATH = pathlib.Path(_filepath).parent
            self.FILENAME = pathlib.Path(_filepath).name

        if self.filepath and not self.filepath.exists():
            msg = f'[CRITICAL]no[{self.filepath=}]'
            raise Exx__FileNotExists(msg)

        if self.filepath:
            self._text = self.filepath.read_text()

    @property
    def filepath(self) -> Optional[pathlib.Path]:
        """compose final pathlib instance for file
        """
        try:
            if self.FILENAME:
                return pathlib.Path(self.DIRPATH, self.FILENAME)
        except:
            pass

    # -----------------------------------------------------------------------------------------------------------------
    def load_dict(self) -> None:
        """load values from source into instance attributes.
        """
        section_dict = self.get_dict()
        self.apply_dict(section_dict)

    def apply_dict(self, attrs: Optional[Dict[str, Any]] = None, update: Optional[bool] = None) -> None | NoReturn:
        """Apply passes dict into instance and check consistence.
        """
        # clear -----------------------
        if self.dict and not update:
            for key in self.dict:
                delattr(self, key)

        # work -----------------------
        if attrs is not None:
            if update:
                self.dict.update(attrs)
            else:
                self.dict = dict(attrs)

        if self.dict is None:
            return

        for key, value in self.dict.items():
            setattr(self, key, value)

    def update_dict(self, attrs: Optional[Dict[str, Any]]) -> None | NoReturn:
        """Apply passes dict into instance and check consistence.
        """
        self.apply_dict(attrs, True)

    def preupdate_dict(self, attrs: Dict[str, Any]) -> None | NoReturn:
        """Apply passes dict into instance and check consistence.
        """
        # prepare  -----------------------
        new_dict = {}
        for key, value in attrs.items():
            if key not in self.dict:
                new_dict.update({key: value})

        # work -----------------------
        self.update_dict(new_dict)

    # -----------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def get_dict(self) -> Optional[Dict[str, Any]]:
        """Obtain existed values from source in dict structure.

        return
            NONE - if no section! dont raise inside!
            {} - if no names!
        """
        pass


# =====================================================================================================================
