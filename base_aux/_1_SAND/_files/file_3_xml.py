# TODO-!!!!!=здесь нужно вообще переделать весь XML на наследование от filepath!!!! только потом будет смысл чтото делать
# TODO-1=переделать сохранение XML на write!!!
# TODO-2=переделать XML pretty

# =====================================================================================================================
# STARICHENKO UNIVERSAL IMPORT
import sys
sys.path.append("..")  # Adds higher directory to python modules path.

import time
from typing import *
import pathlib


from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# from users.user_profile import UserProfile_Singleton
# from stands.stand import Stand_Singleton
# from results.results_testplan import TestplanResults_Singleton
# =====================================================================================================================


from .file_0_selector import File
import os
import _io
import pytest

from xml.dom.minidom import parseString
import xml.etree.ElementTree as ET


class ProcessorXml(File):  # starichenko
    """common Xml wrapper

    ERRORS IMPORTANT:
        1. dont compare direct ELEMENT object with BOOL!!! use clear comparison with NONE!!!
            xml_data = xml_data or self.xml_element     # WRONG!!!
            xml_data = xml_data if xml_data is not None else self.xml_element     # CORRECT!!!
    """
    __xml_element: Optional[ET.Element] = None

    # ELEMENT =========================================================================================================
    @property
    def xml_element(self) -> Optional[ET.Element]:
        return self.__xml_element

    def xml_element__check_empty(self) -> bool:
        return self.xml_element is None

    def xml_element__check_not_empty(self) -> bool:
        return self.xml_element is not None

    def xml_element__get_active(self, xml_data: Any = None) -> Optional[ET.Element]:
        if xml_data is None:
            result = self.xml_element
        else:
            result = self._xml_element__get_from_any(xml_data)

        if result is None:
            msg = f"NO DATA {self.xml_element=}"
            print(msg)
        return result

    def xml_element__set(self, xml_data) -> bool:
        self.__xml_element = self._xml_element__get_from_any(xml_data)
        if self.__xml_element is not None:
            return True
        else:
            msg = f"incorrect input {xml_data=}"
            print(msg)

    def _xml_element__get_from_any(self, xml_data) -> Optional[ET.Element]:
        # PRECHECK -------------------------------------------------
        if xml_data is None:
            msg = f"NO INPUT {xml_data=}"
            print(msg)
            return

        # WORK -------------------------------------------------
        element_obj = None

        if ET.iselement(xml_data):  # 1=ELEMENT=same as isinstance(xml_any_type_data, ET.Element)
            element_obj = xml_data
        elif isinstance(xml_data, ET.ElementTree):  # 2=TREE
            element_obj = xml_data.getroot()
        elif isinstance(xml_data, _io.TextIOWrapper):  # FILE_openObj
            encoding = xml_data.encoding
            if encoding.lower() not in ["utf-8", "utf8"]:
                print(f"file object have incorrect [{encoding=}] may be ERRORS")

            element_obj = self.xml_element__read(xml_data)
        elif isinstance(xml_data, str):  # STR
            if os.path.exists(xml_data):  # str=FILE_NAME
                element_obj = self.xml_element__read(xml_data)
            else:
                try:
                    element_obj = ET.fromstring(xml_data)  # str=STR
                except:
                    msg = f"inputData have no valid XML info!!! {type(xml_data)=}[{xml_data=}]"
                    print(msg)

        elif isinstance(xml_data, bytes):  # BYTES
            element_obj = ET.fromstring(xml_data)

        # FINISH -------------------------------------------------
        if element_obj is None:
            msg = f"NO DATA cant create from {element_obj=}/{type(element_obj)}/{repr(element_obj)}///{xml_data=}/{type(xml_data)=}/{repr(xml_data)=}"
            print(msg)
        return element_obj

    # STRING ==========================================================================================================
    pass

    def xml_element__check_no_decoding_errors(self, xml_data: Any = None) -> bool:
        """ can be only in bytes!
        """
        xml_bytes = self.xml_bytes__get_from_any(xml_data)
        try:
            xml_string = xml_bytes.decode(encoding="utf-8")
            return True
        except Exception as exx:
            msg = f"XML have NONPRINTABLE INCORRECT data!!!\n{exx!r}"
            print(msg)
            msg = f"НЕОБХОДИМО САМОСТОЯТЕЛЬНО НАЙТИ НЕКОРРЕКТНЫЕ ДАННЫЕ И ИХ количество!!!"
            print(msg)

    # BYTES -----------------------------------------------------------------------------------------------------------
    def xml_bytes__get_from_any(self, xml_data: Any = None) -> Union[None, bytes]:
        xml_element = self.xml_element__get_active(xml_data)
        if xml_element is None:
            return
        return ET.tostring(xml_element, encoding="utf-8", xml_declaration=True)

    # STR -------------------------------------------------------------------------------------------------------------
    def xml_string__get_from_any(self, xml_data: Any = None) -> Union[None, str]:
        xml_bytes = self.xml_bytes__get_from_any(xml_data)
        if xml_bytes is None:
            return

        try:
            xml_string = xml_bytes.decode(encoding="utf-8")
        except:
            msg = f"XML have NONPRINTABLE data!!!"
            print(msg)

            xml_string = xml_bytes.decode(encoding="utf-8", errors="ignore")

        return xml_string

    # PRETTY ----------------------------------------------------------------------------------------------------------
    def xml_string_pretty__get_from_any(self, xml_data: Any = None) -> Union[None, str]:
        xml_string = self.xml_string__get_from_any(xml_data)
        if xml_string is None:
            return

        try:
            minidom_document = parseString(xml_string)
            pretty_xml_string = minidom_document.toprettyxml()

            pretty_xml_string = UFU.str_replace_blank_lines(source=pretty_xml_string)
            return pretty_xml_string

        except:
            msg = f"NONPRINTABLE BYTES in XML [{xml_string=}]"
            print(msg)

        return xml_string

    # LOAD/DUMP =======================================================================================================
    def xml_element__read(self, filepath=None) -> Optional[ET.Element]:
        filepath = self.get_active__filepath(filepath)
        if filepath:
            tree_obj = ET.ElementTree(file=filepath)        # WORK WITH FileOpenObject and FileNAME!!!
            element_obj = tree_obj.getroot()
            return element_obj

    def xml_element__load(self, filepath=None) -> Optional[bool]:
        element_obj = self.xml_element__read(filepath)
        if element_obj is not None:
            return self.xml_element__set(element_obj)

    def xml_element__dump(self, xml_data=None, filepath=None) -> Optional[bool]:
        filepath = self.get_active__filepath(filepath)
        if not filepath:
            return

        text = self.xml_string_pretty__get_from_any(xml_data)
        if text is None:
            return

        return self.write__text(text=text, filepath=filepath)

    # ATTR ============================================================================================================
    def xml_element_attr__get_dict(self, xml_data=None):
        """retern element attribute dict

        :return: type always DICT!!!
        """
        xml_element = self.xml_element__get_active(xml_data)
        if hasattr(xml_element, "attrib"):
            element_attr_dict = xml_element.attrib
        else:
            element_attr_dict = {}
        return element_attr_dict

    def xml_element_attr__get_value(self, name, xml_data=None):
        """retern element attribute value

        :return: exact value if have name
        """
        xml_element = self.xml_element__get_active(xml_data)
        element_attr_dict = self.xml_element_attr__get_dict(xml_element)
        if not element_attr_dict:
            return
        return element_attr_dict.get(name)

    # DICT ============================================================================================================
    # TODO: need tests!!!
    def xml_dict__get_simple_no_conflict_elements(self, xml_data=None, only_one_level: bool = False) -> dict:   # starichenko
        """
        get dict from element
        simple expected keys and values!
        without attributes - will not parse!
        :return:

        EXAMPLE
        	<tag1>val1</tag1>
            <tag2>val2</tag2>
            <tag>val</tag>
            <tag>val</tag>
            <IMAGES_INFO>
                <DIR_EXIST>1</DIR_EXIST>
                <IMAGE>
                    <NAME>image-2</NAME>
                </IMAGE>
                <IMAGE>
                    <NAME>image-1</NAME>
                    ///
        return {
            tag1: val1
            tag2: val2
        }
        """
        xml_element = self.xml_element__get_active(xml_data)

        result = {}
        for element in xml_element:
            key = element.tag

            # prepare value -----------------------
            if len(element) == 0:
                value = element.text or ""
                value = value.strip()
            else:
                if only_one_level:
                    continue
                else:
                    value = self.xml_dict__get_simple_no_conflict_elements(element)

            # add key to dict -----------------
            if key not in result or value == result.get(key):
                result[key] = value
            else:
                result.pop(key)
                msg = f"conflict {key=}/{value=} already exists not equel [{result.get(key)}]"
                print(msg)

        return result

    def xml_dict__get(self, xml_data=None, key_attr="_attrib", key_text="_text", use_root_element=False):
        result_dict = {}

        xml_element = self.xml_element__get_active(xml_data)
        for element in self.xml_elements__iter(xml_data=xml_element, only_direct_childs=True):
            key = element.tag

            # VALUE ---------------------------
            value_attr = element.attrib
            value_elements = self.xml_dict__get(xml_data=element, key_attr=key_attr, key_text=key_text, use_root_element=False)
            value_text = element.text
            if UFU.value_is_blanked(value_text):
                value_text = ""
            result_dict.update({key: {key_attr: value_attr, key_text: value_text, **value_elements}})

        if use_root_element:
            root_attr = self.xml_element.attrib
            root_text = self.xml_element.text
            if UFU.value_is_blanked(root_text):
                root_text = ""
            result_dict = {self.xml_element.tag: {key_attr: root_attr, key_text: root_text, **result_dict}}

        return result_dict

    # ITER ============================================================================================================
    def xml_elements__iter(self, xml_data=None, xpath=None, only_direct_childs=False, _print=False, use_root=False):  # starichenko
        """
        iter_elements in xml_data!
            for Tree-obj - gives all elements with zeroLevel
            for root/Element-obj - gives only child inserted elements!!! without zeroLevel

        WHY USE IT
            1. usuall element.iter() gives you all elements including zerolevel!!! --maybe use iter("./")????


        :xml_data: use any Tree/Element-obj - for all gives same result!!!
            BUT if use Tree-obj - use only only_direct_childs=True!!!! otherwise get error!&&&&&
        :xpath: if specified - show elements with only exact name
            в xpath НЕТ МАСОК НА ИМЕНА!!!! есть только на пути!!!
        :only_direct_childs: if False - walk all structure!

            example of nested-result:
                element=<Element 'rootElement' at 0x0000017FFF6135E0> text=[None]
                element=<Element 'item' at 0x0000013C3103C4F0> text=[None]
                element=<Element 'textElement' at 0x0000017FFF61C4F0> text=[Text in textElement]
                element=<Element 'listElement' at 0x0000017FFF61CF40> text=[None]
                element=<Element 'item' at 0x0000017FFF62DA90> text=[1]
                element=<Element 'item' at 0x0000017FFF774AE0> text=[2]
                element=<Element 'item' at 0x0000017FFF774B80> text=[3]
        """
        result_list = []

        xml_element = self.xml_element__get_active(xml_data)

        if xml_element is None:
            return result_list

        if not xpath:
            xpath = ""

        if only_direct_childs:
            element_mask = f"./{xpath}"
        else:
            if xpath:
                element_mask = f".//{xpath}"    # for all nested childs! +
            else:
                element_mask = f".//*"
                # self.xml_element.iter("")     # НИЧЕГО НЕ НАЙДЕТ!!!!!
        result_list = xml_element.findall(element_mask)
        # print(f"{result_list=}")

        if _print:
            print("="*100)
            for element in result_list:
                print(f"{element=} [{element.text=}]")
            print("="*100)

        return result_list

    # FIND ============================================================================================================
    def xml_element__find_first(
            self,
            xml_data=None,
            xpath: str = None,
            return_element_text: bool = False,
            walk_nested: bool = True
    ):
        """retern element found first"""
        # INPUT --------------------------------------------------
        if walk_nested:
            xpath = xpath.lstrip("./")
            xpath = f".//{xpath}"

        xml_element = self.xml_element__get_active(xml_data)

        # WORK --------------------------------------------------
        result = None

        if xml_element is not None:
            if return_element_text:
                result = xml_element.findtext(xpath)
            else:
                result = xml_element.find(xpath)

        print(f"[{xpath=}/{result=}]", result=result is not None)
        return result


# TESTS ===============================================================================================================
TEST_XML_SIMPLE_STRING = """
    <tag0 attr1="attr1" attr2="attr2">
        <tag1a attr1="attr1" attr2="attr2">tag1atext</tag1a>
        <tag1b>tag1btext</tag1b>
        <tag1c>
            <tag2a></tag2a>
        </tag1c>
    </tag0>
"""
TEST_XML_SIMPLE_STRING_REPEATS = """
    <tag0 attr1="attr1" attr2="attr2">
        <tag1a attr1="attr1" attr2="attr2">tag1atext</tag1a>
        <tag1b>tag1btext</tag1b>
        <tag1b>tag1btext</tag1b>
        <tag1c>
            <tag2a></tag2a>
        </tag1c>
    </tag0>
"""
TEST_XML_LOGIN_STRING = """
    <RACK Action="Authorize" Result="OK" ErrorCode="0" Msg="">
        HELLO
        <LOGIN>SuperUser</LOGIN>
        <PERMISSIONS>
            <PRM>ParamRead</PRM>
            <PRM>ParamWrite</PRM>
            <PRM>MaskRead</PRM>
        </PERMISSIONS>
    </RACK>
"""
TEST_XML_LOGIN_BYTES = bytes(TEST_XML_LOGIN_STRING, encoding="utf-8")
TEST_XML_LOGIN_ELEMENT = ET.fromstring(TEST_XML_LOGIN_STRING)
TEST_XML_LOGIN_TREE = ET.ElementTree(TEST_XML_LOGIN_ELEMENT)
TEST_XML_LOGIN_FILENAME = f"-TEST_XML_LOGIN_FILENAME.xml"

TEST_XML_LOGIN_atr_DICT = dict(Action="Authorize", Result="OK", ErrorCode="0", Msg="")

@pytest.mark.parametrize(
    argnames="p1,_EXPECTED",
    argvalues=[
        (None, None),
        (123, None),
        ("123", None),

        (TEST_XML_LOGIN_STRING, TEST_XML_LOGIN_ELEMENT),                            # string
        (bytes(TEST_XML_LOGIN_STRING, encoding="utf-8"), TEST_XML_LOGIN_ELEMENT),   # bytes
        (ET.fromstring(TEST_XML_LOGIN_STRING), TEST_XML_LOGIN_ELEMENT),            # element
        (TEST_XML_LOGIN_TREE, TEST_XML_LOGIN_ELEMENT),                              # TREE
    ]
)
def test__xml_element_set(p1,_EXPECTED):
    test_obj_link = ProcessorXml().xml_element__set
    result = test_obj_link(xml_data=p1)
    assert type(result) == type(_EXPECTED)


def test__xml_element_set__file():
    TEST_XML_LOGIN_TREE.write(TEST_XML_LOGIN_FILENAME)
    file_open = open(TEST_XML_LOGIN_FILENAME)

    class_obj = ProcessorXml()

    test_obj_link = class_obj.xml_element__set
    result = test_obj_link(xml_data=file_open)
    assert type(result) == type(TEST_XML_LOGIN_ELEMENT)     # FILE OPEN

    result = test_obj_link(xml_data=TEST_XML_LOGIN_FILENAME)
    assert type(result) == type(TEST_XML_LOGIN_ELEMENT)     # FILE NAME

    file_open.close()


@pytest.mark.parametrize(
    argnames="p1,_EXPECTED",
    argvalues=[
        (None, None),
        (123, None),
        ("123", None),

        (TEST_XML_LOGIN_STRING, TEST_XML_LOGIN_BYTES),                            # string
        (bytes(TEST_XML_LOGIN_STRING, encoding="utf-8"), TEST_XML_LOGIN_BYTES),   # bytes
        (ET.fromstring(TEST_XML_LOGIN_STRING), TEST_XML_LOGIN_BYTES),            # element
        (TEST_XML_LOGIN_TREE, TEST_XML_LOGIN_BYTES),                              # TREE

    ]
)
def test__xml_element_get_bytes(p1,_EXPECTED):
    test_obj_link = ProcessorXml().xml_bytes__get_from_any
    result = test_obj_link(xml_data=p1)
    assert type(result) == type(_EXPECTED)


def test__xml_element_attr_get_dict():
    test_obj_link = ProcessorXml().xml_element_attr__get_dict
    result = test_obj_link(xml_data=TEST_XML_LOGIN_STRING)
    assert result == TEST_XML_LOGIN_atr_DICT     # ATR DICT


@pytest.mark.parametrize(
    argnames="p1,p2,_EXPECTED",
    argvalues=[
        (None, "Action", None),
        (123, "Action", None),
        ("123", "Action", None),

        (TEST_XML_LOGIN_STRING, "Action", "Authorize"),
        (TEST_XML_LOGIN_STRING, "Action123", None),
    ]
)
def test__xml_element_attr_get_value(p1,p2,_EXPECTED):
    test_obj_link = ProcessorXml().xml_element_attr__get_value
    result = test_obj_link(xml_data=p1, name=p2)
    assert result == _EXPECTED


@pytest.mark.parametrize(
    argnames="p1,p2,p3,p4,_EXPECTED",
    argvalues=[

        # trivial
        (None, "base", True, False, None),
        (None, ".//base", True, False, None),
        ("<>", "base", True, True, None),
        ("", "base", True, True, None),

        # опредлеляемся с тегами
        ("<><t2>11</t2></>", "t2", True, True, None),  # НЕ ВОСПРИНИМАЕТ ТЕГ С ПУСТЫМ ИМЕНЕМ!!! - НУЖНО ХТЬ ЧТОТО!!!
        ("<_><t2>11</t2></_>", "t2", True, True, "11"),

        ("<_><t></_>", "t", True, True, ""),
        ("<_><t></t></_>", "t", True, True, ""),
        ("<_><t> </t></_>", "t", True, True, " "),
        ("<_><t>1/2</t></_>", "t", True, True, "1/2"),


        ("<base>", "base",          True, True, ""),        # must return ""
        ("<base></base>", "base",   True, True, ""),        # must return ""
        ("<base> </base>", "base",  True, True, " "),
        ("<base>1</base>", "base",  True, True, "1"),




        (TEST_XML_LOGIN_ELEMENT, "RACK", True, False, None),

        (TEST_XML_LOGIN_ELEMENT, "LOGIN", True, False, "SuperUser"),
        (TEST_XML_LOGIN_ELEMENT, "LOGIN", True, True, "SuperUser"),
        (TEST_XML_LOGIN_ELEMENT, ".//LOGIN", True, True, "SuperUser"),

        (TEST_XML_LOGIN_ELEMENT, "PRM", True, False, None),
        (TEST_XML_LOGIN_ELEMENT, "PRM", True, True, "ParamRead"),
    ]
)
def test__xml_find_element_first(p1,p2,p3,p4,_EXPECTED):
    test_obj_link = ProcessorXml().xml_element__find_first
    result = test_obj_link(xml_data=p1, xpath=p2, return_element_text=p3, walk_nested=p4)
    assert result == _EXPECTED


@pytest.mark.parametrize(
    argnames="p1,p2,p3,p4,_EXPECTED",
    argvalues=[
        # only_direct_childs=True
        (TEST_XML_SIMPLE_STRING, None,    True, False, ["tag1a", "tag1b", "tag1c"]),
        (TEST_XML_SIMPLE_STRING, "tag1a", True, False, ["tag1a"]),
        (TEST_XML_SIMPLE_STRING, "tag2a", True, False, []),

        # only_direct_childs=False
        (TEST_XML_SIMPLE_STRING, None,    False, False, ["tag1a", "tag1b", "tag1c", "tag2a"]),
        (TEST_XML_SIMPLE_STRING, "tag1a", False, False, ["tag1a"]),
        (TEST_XML_SIMPLE_STRING, "tag1", False, False, []),
        (TEST_XML_SIMPLE_STRING, "tag1*", False, False, []),    # в xpath НЕТ МАСОК НА ИМЕНА!!!! есть только на пути!!!

    ]
)
def test__xml_elements_iter(p1,p2,p3,p4,_EXPECTED):
    test_obj_link = ProcessorXml().xml_elements__iter
    result = test_obj_link(xml_data=p1, xpath=p2, only_direct_childs=p3, _print=p4)
    result_list = [i.tag for i in result]
    assert result_list == _EXPECTED


@pytest.mark.parametrize(
    argnames="p1,p2,p3,p4,_EXPECTED",
    argvalues=[
        ("""
            <tag0 attr1="attr1">
            </tag0>
            """, "_attr", "_text", False, {}),
        ("""
            <tag0 attr1="attr1">
                <tag1a></tag1a>
            </tag0>
            """, "_attr", "_text", True, {"tag0": {"_attr": {"attr1": "attr1"}, "_text": "", "tag1a": {"_attr": {}, "_text": ""}}}),

        ("""
            <tag0 attr1="attr1">
                <tag1a></tag1a>
            </tag0>
            """, "_attr", "_text", False, {"tag1a": {"_attr": {}, "_text": ""}}),

        # ("""
        # <tag0 attr1="attr1" attr2="attr2">
        #     <tag1a attr1="attr1" attr2="attr2">tag1atext</tag1a>
        #     <tag1b>tag1btext</tag1b>
        #     <tag1c>
        #         <tag2a></tag2a>
        #     </tag1c>
        # </tag0>
        # """, None,    None, True, {"tag0": {"tag1a": "tag1atext", "tag1b": "tag1btext", "tag1c": {"tag2a": ""}}}),

    ]
)
def test__xml_dict_get(p1,p2,p3,p4,_EXPECTED):
    test_obj_link = ProcessorXml().xml_dict__get
    result = test_obj_link(xml_data=p1, key_attr=p2, key_text=p3, use_root_element=p4)
    assert result == _EXPECTED


@pytest.mark.parametrize(
    argnames="p1,p2,_EXPECTED",
    argvalues=[
        (TEST_XML_LOGIN_STRING, True, {"LOGIN": "SuperUser"}),
        (TEST_XML_SIMPLE_STRING_REPEATS, True, {'tag1a': 'tag1atext', 'tag1b': 'tag1btext'}),
]
)
def test__xml_dict_get_simple_no_conflict_elements(p1,p2,_EXPECTED):
    test_obj_link = ProcessorXml().xml_dict__get_simple_no_conflict_elements
    result = test_obj_link(xml_data=p1, only_one_level=p2)
    assert result == _EXPECTED


def test__xml_string_pretty__get_from_any():
    obj = ProcessorXml()
    obj.filepath_set("_GDDU_nonprintable.xml")
    obj.xml_element__load()
    print(obj.xml_string_pretty__get_from_any())


def main_starichenko():
    class_obj = ProcessorXml()
    test_obj_link = class_obj.xml_elements__iter
    result = test_obj_link(xml_data=TEST_XML_LOGIN_BYTES, _print=True)
    for element in list(result):
        print(f"{element=}")
    print(f"{result=}")


# =====================================================================================================================
if __name__ == '__main__':
    main_starichenko()


# =====================================================================================================================
