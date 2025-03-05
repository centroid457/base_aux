import abc

from base_aux.aux_attr.m2_annot1_aux import *
from base_aux.base_statics.m1_types import *
from base_aux.aux_attr.m1_attr2_nest1_gsai_anycase import *


# =====================================================================================================================
# TODO: add iter???


# =====================================================================================================================
class PrivateBase(NestGAI_AttrIC, abc.ABC):
    """Base class to get values from sources.

    :ivar SECTION: first level name in source, for ini - root section, for json - rootKey, for env - not used
    :ivar DIRPATH: file destination
    :ivar FILENAME: file name

    USAGE
    -----
    if you dont need RAISE when no value get for exact annotated name - just define None!
    """
    _RAISE: Optional[bool] = True

    SECTION: Optional[str] = None

    DIRPATH: TYPING.PATH_FINAL = pathlib.Path.home()
    FILENAME: Optional[str] = None

    _text: Optional[str] = ""     # TODO: need tests!!!
    DICT: dict[str, Any] = None

    # -----------------------------------------------------------------------------------------------------------------
    def __init__(
            self,
            _section: Optional[str] = None,

            _dirpath: TYPING.PATH_DRAFT = None,
            _filename: str = None,
            _filepath: TYPING.PATH_DRAFT = None,

            _text: Optional[str] = None,                # instead of file
            _dict: Optional[dict[str, Any]] = None,     # instead of file

            _raise: Optional[bool] = None
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
            if not self._filepath_apply_new(
                _dirpath=_dirpath,
                _filename=_filename,
                _filepath=_filepath
            ):
                return

        if _dict is None:
            self.load_dict()

        if _raise is not None:
            self._RAISE = _raise

        if self._RAISE:
            AnnotAttrAux(self).check_all_defined_or_raise()

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
    @classmethod
    def file_check_exists(cls) -> bool:
        """
        SPECIALLY CREATED FOR
        ---------------------
        for pytest when i use Privates
        i need to skip tests when i have no Privates! like in githubActions or on workPC

        by now just use
            @pytest.mark.skipif(Lambda().check_raise(), reason="no file")
        """
        pass
        # FIXME: finish when pigs fly!

    def _filepath_apply_new(
            self,
            _dirpath: TYPING.PATH_DRAFT = None,
            _filename: str = None,
            _filepath: TYPING.PATH_DRAFT = None
    ) -> bool:
        """apply new file destination
        """
        if not _filepath:
            self.DIRPATH = pathlib.Path(_dirpath or self.DIRPATH)
            self.FILENAME = _filename or self.FILENAME
        else:
            self.DIRPATH = pathlib.Path(_filepath).parent
            self.FILENAME = pathlib.Path(_filepath).name

        if self.filepath and not self.filepath.exists():
            if self._RAISE:
                raise FileNotFoundError(f'{self.filepath=}')
            else:
                return False

        if self.filepath:
            self._text = self.filepath.read_text()

        return True

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

    def apply_dict(self, attrs: Optional[dict[str, Any]] = None, update: Optional[bool] = None) -> None | NoReturn:
        """Apply passes dict into instance and check consistence.
        """
        # clear -----------------------
        if self.DICT and not update:
            for key in self.DICT:
                delattr(self, key)

        # work -----------------------
        if attrs is not None:
            if update:
                self.DICT.update(attrs)
            else:
                self.DICT = dict(attrs)

        if self.DICT is None:
            return

        for key, value in self.DICT.items():
            setattr(self, key, value)

    def update_dict(self, attrs: Optional[dict[str, Any]]) -> None | NoReturn:
        """Apply passes dict into instance and check consistence.
        """
        self.apply_dict(attrs, True)

    def preupdate_dict(self, attrs: dict[str, Any]) -> None | NoReturn:
        """Apply passes dict into instance and check consistence.
        """
        # prepare  -----------------------
        new_dict = {}
        for key, value in attrs.items():
            if key not in self.DICT:
                new_dict.update({key: value})

        # work -----------------------
        self.update_dict(new_dict)

    # -----------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def get_dict(self) -> Optional[dict[str, Any]]:
        """Obtain existed values from source in dict structure.

        return
            NONE - if no section! dont raise inside!
            {} - if no names!
        """
        pass


# =====================================================================================================================
