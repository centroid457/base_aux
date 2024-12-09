# TODO-1: maybe ref all to more simple&
# TODO: ref all signals into one with [int]

# =====================================================================================================================
from typing import *

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import time
from threading import Thread
from base_aux.objects import LAMBDA_TRUE, SLEEP_TRUE
from base_aux.pyqt.static import COLOR_TUPLE_RGB


# SET ============================================================================================================
class DialogsSet:
    """
    attempt to keep all available dialogs for current project in one place!
    so to be sure there are no any other available!
    """
    @staticmethod
    def info__about(*args) -> int:
        answer = QMessageBox.information(
            None,
            "About Program",
            (
                "LLC CompanyName,\n"
                "Program name\n"
                "(purpose)"
             )
        )
        # return always 1024
        return answer


# SIMPLEST ============================================================================================================
def try__info():
    app = QApplication([])
    print(DialogsSet.info__about())
    app.exec()


# OTHERS ==============================================================================================================
class MessageDialog(QDialog):   # Шихалиев???
    """
    just found in corporate repo from not a really programming department
    """
    def __init__(self, text, parent=None):
        super(MessageDialog, self).__init__(parent)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(text))

        # OK and Cancel buttons
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        layout.addWidget(self.buttons)

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

    # static method to create the dialog and return (date, time, accepted)
    @staticmethod
    def info(text, parent=None):
        dialog = MessageDialog(text, parent)
        result = dialog.exec_()
        return (result == QDialog.Accepted)


# =====================================================================================================================
class GuiDialog(QWidget):
    """
    allow to use Gui Interactive from independent console!

    ATTENTION!!!
        YOU MUST INSTANTIATE OBJECT IN MAIN THREAD!!!
        SO IT WILL BE WORKING IN ANY THREAD!!! otherwise will not!
        dont need to save it! only start!

    IMPORTANT:
        1. ALL methods if ask accept/reject must return TRUE if clicked OK/Apply buttons! otherwise False!
        2. first parameter in any

    EXAMPLE usage:
        GuiDialog().simple_1_info()



    FOR AUTOACCEPTION    !!!!!!!!!!!!!!!IN CASE OF FREEZE!!!!!!!!!!!!!!!!!!!
        Only one reason is - incondition state in result of autoaccept_link
        for example
            WRONG -     [GuiDialog().simple_1_info(message, autoaccept_link=lambda: self.fu_get_current_v12())]
            CORRECT -   [GuiDialog().simple_1_info(message, autoaccept_link=lambda: bool(self.fu_get_current_v12()))]
    """
    s_type0 = pyqtSignal(str, str)  # (msg, title)
    s_type1 = pyqtSignal(str, str)
    s_type2 = pyqtSignal(str, str)
    s_type3 = pyqtSignal(str, str)
    s_type4 = pyqtSignal(str, str)
    s_type5 = pyqtSignal(str, str)
    s_type6 = pyqtSignal(str, str)
    s_type7 = pyqtSignal(str, str)

    WGT_ROOT = None  # if contain object - will be used signal!
    WGT_ROOT_NAME = "WGT_ROOT_NAME"

    WGT_NOLOCK_NOANSWER = None

    # def __new__(cls, *args, **kwargs):
    #     if cls.WGT_ROOT is None:
    #         cls.WGT_ROOT = super().__new__(cls, *args, **kwargs)
    #     return super().__new__(cls, *args, **kwargs)

    ANSWER_READY = None
    ANSWER_LAST = None
    ANSWER_LAST_AUTOACCEPTED = None

    def __init__(self, _create_singleton_obj=None):
        """
        :param _create_singleton_obj: DONT USE IT!!! it must start only auto in deep code by self!
        """
        self.app = None

        if _create_singleton_obj:
            self._init_qapplication_or_root_dialog_obj()
            super().__init__()
            self.setObjectName(self.WGT_ROOT_NAME)

            self.s_type0.connect(self._only_simple_0_nolock_noanswer)
            self.s_type1.connect(self._only_simple_1_info)
            self.s_type2.connect(self._only_simple_2_question)
            self.s_type3.connect(self._only_simple_3_critical)
            self.s_type4.connect(self._only_input_string)
            self.s_type5.connect(self._only_select_file)
            self.s_type6.connect(self._only_select_font)
            self.s_type7.connect(self._only_select_color)

        elif __class__.WGT_ROOT is None:
            __class__.WGT_ROOT = __class__(_create_singleton_obj=True)

    # CLOSE/ACCEPT ====================================================================================================
    @classmethod
    def close_wgt_nolock_noanswer(cls):
        cls.WGT_NOLOCK_NOANSWER = None

    @classmethod
    def accept_all_dialogs(cls):
        while True:  # need to accept all Dialogs without overlapping!
            top_level_widgets = QApplication.topLevelWidgets()
            # print(f"{top_level_widgets=}")
            if len(top_level_widgets) > 0:
                for wgt_i in top_level_widgets:
                    # print(f"{wgt_i.objectName()=}/{wgt_i=}")
                    if hasattr(wgt_i,
                               "accept") and wgt_i.parent() and wgt_i.parent().objectName() == cls.WGT_ROOT_NAME:
                        # print(f"ACCEPT-START={wgt_i.parent().objectName()=}/{wgt_i.objectName()=}/{wgt_i=}/{wgt_i.parent()=}")
                        try:
                            time.sleep(0.3)  # without sleep it will work instable!!! ones a 10 steps will get freez!
                            wgt_i.accept()
                        except:
                            pass

                        return
                    # if wgt_i.objectName() == self.WGT_ROOT_NAME:
                    #     print(f"ЗАКРЫТИЕ!!! - СТАРТ")
                    #     wgt_i.close()
                    #     print(f"ЗАКРЫТИЕ!!! - ФИНИШ!!!")
            break
        return True

    @classmethod
    def autoaccept_start_thread(cls, autoaccept_func_link):
        thread = Thread(target=lambda: cls.autoaccept_start(autoaccept_func_link), daemon=True)
        thread.start()

    @classmethod
    def autoaccept_start(cls, autoaccept_func_link):
        """close all dialogs in all threads!!!"""
        result = False
        while not cls.ANSWER_READY:
            try:
                result = autoaccept_func_link()
            except:
                pass

            if result:
                cls.accept_all_dialogs()
                cls.ANSWER_LAST_AUTOACCEPTED = result
                return True
            else:
                time.sleep(1)

    # =================================================================================================================
    def _init_qapplication_or_root_dialog_obj(self):
        """
        init QApplication only if was not called! otherwise will incorrect working at sequence starting!!!
        :return:

        CHECK:
            enaugh only on one Thread project!!!
                QApplication.applicationName() - on child thread will show not blank!!!
                QApplication.hasPendingEvents() - on child thread will show False!!!


            # print("111111111111\n"*10)
            # UFU.obj_show_attr_all(QApplication, miss_names=["aboutQt", "beep", "fontMetrics", "pyqtConfigure", "exec", "exec_"])
            ////////////////////////////////////////////////// obj_show_attr_all //////////////////////////////////////////////////
            ////////// _parents_list=[] nested_level=[0] source=<class 'PyQt5.QtWidgets.QApplication'> //////////
            meth=[.ColorSpec]                       value=[0]
            attr=[.CustomColor]                     value=[1]
            attr=[.ManyColor]                       value=[2]
            attr=[.NormalColor]                     value=[0]
            meth=[.__class__]                       value=[<class 'sip.wrappertype'>]
            attr=[.__delattr__]                     value=[***MISSED DANGER***]
            obj=[.__dict__]                         value=[{'__module__': 'PyQt5.QtWidgets', '__doc__': 'QApplication(List[str])', 'ColorSpec': <class 'PyQt5.QtWidgets.QApplication.ColorSpec'>, 'aboutQt': <built-in method aboutQt>, 'activeModalWidget': <built-in method activeModalWidget>, 'activePopupWidget': <built-in method activePopupWidget>, 'activeWindow': <built-in method activeWindow>, 'alert': <built-in method alert>, 'allWidgets': <built-in method allWidgets>, 'autoSipEnabled': <built-in method autoSipEnabled>, 'beep': <built-in method beep>, 'childEvent': <built-in method childEvent>, 'closeAllWindows': <built-in method closeAllWindows>, 'colorSpec': <built-in method colorSpec>, 'connectNotify': <built-in method connectNotify>, 'cursorFlashTime': <built-in method cursorFlashTime>, 'customEvent': <built-in method customEvent>, 'desktop': <built-in method desktop>, 'disconnectNotify': <built-in method disconnectNotify>, 'doubleClickInterval': <built-in method doubleClickInterval>, 'event': <built-in method event>, 'exec': <built-in method exec>, 'exec_': <built-in method exec_>, 'focusWidget': <built-in method focusWidget>, 'font': <built-in method font>, 'fontMetrics': <built-in method fontMetrics>, 'globalStrut': <built-in method globalStrut>, 'isEffectEnabled': <built-in method isEffectEnabled>, 'isSignalConnected': <built-in method isSignalConnected>, 'keyboardInputInterval': <built-in method keyboardInputInterval>, 'notify': <built-in method notify>, 'palette': <built-in method palette>, 'receivers': <built-in method receivers>, 'sender': <built-in method sender>, 'senderSignalIndex': <built-in method senderSignalIndex>, 'setActiveWindow': <built-in method setActiveWindow>, 'setAutoSipEnabled': <built-in method setAutoSipEnabled>, 'setColorSpec': <built-in method setColorSpec>, 'setCursorFlashTime': <built-in method setCursorFlashTime>, 'setDoubleClickInterval': <built-in method setDoubleClickInterval>, 'setEffectEnabled': <built-in method setEffectEnabled>, 'setFont': <built-in method setFont>, 'setGlobalStrut': <built-in method setGlobalStrut>, 'setKeyboardInputInterval': <built-in method setKeyboardInputInterval>, 'setPalette': <built-in method setPalette>, 'setStartDragDistance': <built-in method setStartDragDistance>, 'setStartDragTime': <built-in method setStartDragTime>, 'setStyle': <built-in method setStyle>, 'setStyleSheet': <built-in method setStyleSheet>, 'setWheelScrollLines': <built-in method setWheelScrollLines>, 'setWindowIcon': <built-in method setWindowIcon>, 'startDragDistance': <built-in method startDragDistance>, 'startDragTime': <built-in method startDragTime>, 'style': <built-in method style>, 'styleSheet': <built-in method styleSheet>, 'timerEvent': <built-in method timerEvent>, 'topLevelAt': <built-in method topLevelAt>, 'topLevelWidgets': <built-in method topLevelWidgets>, 'wheelScrollLines': <built-in method wheelScrollLines>, 'widgetAt': <built-in method widgetAt>, 'windowIcon': <built-in method windowIcon>, 'CustomColor': 1, 'ManyColor': 2, 'NormalColor': 0, 'focusChanged': <unbound PYQT_SIGNAL focusChanged(QWidget*,QWidget*)>}]
            meth=[.__dir__]                         value=[<method '__dir__' of 'object' objects>]
            attr=[.__doc__]                         value=[QApplication(List[str])]
            attr=[.__enter__]                       value=[***MISSED DANGER***]
            meth=[.__eq__]                          value=[<slot wrapper '__eq__' of 'object' objects>]
            attr=[.__exit__]                        value=[***MISSED DANGER***]
            meth=[.__format__]                      value=[<method '__format__' of 'object' objects>]
            meth=[.__ge__]                          value=[<slot wrapper '__ge__' of 'object' objects>]
            meth=[.__getattr__]                     value=[<built-in function __getattr__>]
            meth=[.__getattribute__]                value=[<slot wrapper '__getattribute__' of 'object' objects>]
            meth=[.__gt__]                          value=[<slot wrapper '__gt__' of 'object' objects>]
            meth=[.__hash__]                        value=[<slot wrapper '__hash__' of 'object' objects>]
            attr=[.__init__]                        value=[***MISSED DANGER***]
            attr=[.__init_subclass__]               value=[***MISSED DANGER***]
            meth=[.__le__]                          value=[<slot wrapper '__le__' of 'object' objects>]
            meth=[.__lt__]                          value=[<slot wrapper '__lt__' of 'object' objects>]
            attr=[.__module__]                      value=[PyQt5.QtWidgets]
            meth=[.__ne__]                          value=[<slot wrapper '__ne__' of 'object' objects>]
            attr=[.__new__]                         value=[***MISSED DANGER***]
            attr=[.__reduce__]                      value=[***MISSED DANGER***]
            attr=[.__reduce_ex__]                   value=[***MISSED DANGER***]
            meth=[.__repr__]                        value=[<slot wrapper '__repr__' of 'object' objects>]
            attr=[.__setattr__]                     value=[***MISSED DANGER***]
            meth=[.__sizeof__]                      value=[<method '__sizeof__' of 'object' objects>]
            meth=[.__str__]                         value=[<slot wrapper '__str__' of 'object' objects>]
            meth=[.__subclasshook__]                value=[NotImplemented]
            obj=[.__weakref__]                      value=[<attribute '__weakref__' of 'QObject' objects>]
            attr=[.aboutQt]                         value=[***MISSED SPECIAL***]
            meth=[.aboutToQuit]                     value=[<unbound PYQT_SIGNAL aboutToQuit()>]
            meth=[.activeModalWidget]               value=[None]
            meth=[.activePopupWidget]               value=[None]
            meth=[.activeWindow]                    value=[<gui.main_widget.TestSystemWidget object at 0x000002880E8FAA60>]
            meth=[.addLibraryPath]                  value=[<built-in function addLibraryPath>]
            meth=[.alert]                           value=[<built-in function alert>]
            meth=[.allWidgets]                      value=[[<PyQt5.QtWidgets.QScrollBar object at 0x0000028811F158B0>, <PyQt5.QtWidgets.QLabel object at 0x0000028810BB5DC0>, <PyQt5.QtWidgets.QWidget object at 0x0000028811F15820>, <PyQt5.QtWidgets.QScrollBar object at 0x0000028811F15670>, <PyQt5.QtWidgets.QWidget object at 0x0000028811F15700>, <PyQt5.QtWidgets.QWidget object at 0x0000028811F159D0>, <PyQt5.QtWidgets.QHeaderView object at 0x0000028811F15A60>, <PyQt5.QtWidgets.QWidget object at 0x0000028811F15790>, <PyQt5.QtWidgets.QWidget object at 0x0000028811F155E0>, <PyQt5.QtWidgets.QSplitter object at 0x000002880EA21550>, <PyQt5.QtWidgets.QWidget object at 0x0000028811F15940>, <gui.authorization_widget.WidgetServerAuthorization object at 0x000002881306CF70>, <PyQt5.QtWidgets.QLabel object at 0x0000028810BBBEE0>, <PyQt5.QtWidgets.QPushButton object at 0x000002880EA00EE0>, <PyQt5.QtWidgets.QPushButton object at 0x000002880EA00790>, <PyQt5.QtWidgets.QFrame object at 0x0000028810BBBB80>, <PyQt5.QtWidgets.QFrame object at 0x0000028811F15550>, <PyQt5.QtWidgets.QPushButton object at 0x000002880EA21700>, <PyQt5.QtWidgets.QPushButton object at 0x000002880EA00A60>, <PyQt5.QtWidgets.QHeaderView object at 0x0000028811F15AF0>, <PyQt5.QtWidgets.QHeaderView object at 0x0000028811F15B80>, <PyQt5.QtWidgets.QWidget object at 0x0000028811F15C10>, <PyQt5.QtWidgets.QScrollBar object at 0x0000028811F15CA0>, <PyQt5.QtWidgets.QLabel object at 0x0000028811F15D30>, <PyQt5.QtWidgets.QFrame object at 0x0000028810BB83A0>, <PyQt5.QtWidgets.QLabel object at 0x0000028810BB80D0>, <gui.widget_progress_bar.WidgetProgressBar object at 0x0000028810BBBDC0>, <PyQt5.QtWidgets.QFrame object at 0x0000028811F15DC0>, <PyQt5.QtWidgets.QWidget object at 0x0000028811F15E50>, <PyQt5.QtWidgets.QLabel object at 0x0000028810BB5B80>, <PyQt5.QtWidgets.QScrollBar object at 0x0000028811F15EE0>, <PyQt5.QtWidgets.QCheckBox object at 0x0000028810BBBAF0>, <PyQt5.QtWidgets.QWidget object at 0x0000028810BBB040>, <PyQt5.QtWidgets.QSplitterHandle object at 0x0000028811F15F70>, <PyQt5.QtWidgets.QPushButton object at 0x0000028810BBB9D0>, <PyQt5.QtWidgets.QPushButton object at 0x000002880EA21940>, <PyQt5.QtWidgets.QSplitterHandle object at 0x0000028811D57040>, <PyQt5.QtWidgets.QPushButton object at 0x0000028810BB5790>, <PyQt5.QtWidgets.QLabel object at 0x0000028810BC1040>, <PyQt5.QtWidgets.QSplitter object at 0x000002880E8FAB80>, <PyQt5.QtWidgets.QLineEdit object at 0x0000028811D570D0>, <PyQt5.QtWidgets.QSplitterHandle object at 0x0000028811D57160>, <PyQt5.QtWidgets.QLabel object at 0x0000028810BB5940>, <PyQt5.QtWidgets.QListView object at 0x0000028811D571F0>, <PyQt5.QtWidgets.QLabel object at 0x0000028810BB8310>, <PyQt5.QtWidgets.QPushButton object at 0x0000028810BBBD30>, <PyQt5.QtWidgets.QWidget object at 0x0000028811D57280>, <PyQt5.QtWidgets.QPushButton object at 0x0000028810BBB4C0>, <PyQt5.QtWidgets.QWidget object at 0x0000028811D57310>, <PyQt5.QtWidgets.QPushButton object at 0x0000028810BB54C0>, <PyQt5.QtWidgets.QWidget object at 0x0000028811D573A0>, <PyQt5.QtWidgets.QPushButton object at 0x0000028813089550>, <PyQt5.QtWidgets.QDesktopWidget object at 0x0000028811D57430>, <PyQt5.QtWidgets.QPushButton object at 0x0000028810BB5310>, <PyQt5.QtWidgets.QLabel object at 0x0000028810BB8A60>, <PyQt5.QtWidgets.QScrollBar object at 0x0000028811D574C0>, <PyQt5.QtWidgets.QLabel object at 0x0000028810BB5A60>, <PyQt5.QtWidgets.QPushButton object at 0x0000028810BBB550>, <PyQt5.QtWidgets.QPushButton object at 0x000002880EA21D30>, <PyQt5.QtWidgets.QLabel object at 0x0000028810BB5D30>, <PyQt5.QtWidgets.QPushButton object at 0x0000028810BBB820>, <PyQt5.QtWidgets.QProgressBar object at 0x0000028810BBB1F0>, <PyQt5.QtWidgets.QWidget object at 0x0000028811D57550>, <PyQt5.QtWidgets.QScrollBar object at 0x0000028811D575E0>, <PyQt5.QtWidgets.QLabel object at 0x0000028810BB5E50>, <PyQt5.QtWidgets.QWidget object at 0x0000028811D57670>, <PyQt5.QtWidgets.QAbstractButton object at 0x0000028811D57700>, <PyQt5.QtWidgets.QWidget object at 0x0000028811D57790>, <PyQt5.QtWidgets.QCheckBox object at 0x0000028810BB8CA0>, <PyQt5.QtWidgets.QComboBox object at 0x0000028810BC1280>, <PyQt5.QtWidgets.QLabel object at 0x000002880EA215E0>, <PyQt5.QtWidgets.QPushButton object at 0x0000028810BBBA60>, <PyQt5.QtWidgets.QScrollBar object at 0x0000028811D57820>, <PyQt5.QtWidgets.QScrollBar object at 0x0000028811D578B0>, <PyQt5.QtWidgets.QLabel object at 0x0000028810BB5820>, <PyQt5.QtWidgets.QLabel object at 0x0000028810BB8160>, <PyQt5.QtWidgets.QLabel object at 0x0000028810BB5550>, <PyQt5.QtWidgets.QWidget object at 0x0000028811D57940>, <PyQt5.QtWidgets.QLabel object at 0x0000028813089310>, <gui.stand_settings_edit_widget.WidgetStandSettings object at 0x000002880EA21040>, <PyQt5.QtWidgets.QSplitterHandle object at 0x0000028811D579D0>, <PyQt5.QtWidgets.QWidget object at 0x0000028811D57A60>, <PyQt5.QtWidgets.QScrollBar object at 0x0000028811D57AF0>, <PyQt5.QtWidgets.QLabel object at 0x0000028813089040>, <PyQt5.QtWidgets.QComboBox object at 0x0000028810BB5670>, <PyQt5.QtWidgets.QSplitterHandle object at 0x0000028811D57B80>, <PyQt5.QtWidgets.QWidget object at 0x0000028811D57C10>, <PyQt5.QtWidgets.QWidget object at 0x0000028811D57CA0>, <PyQt5.QtWidgets.QFrame object at 0x0000028811D57D30>, <PyQt5.QtWidgets.QWidget object at 0x0000028811D57DC0>, <gui.widget_stand.WgtStand object at 0x000002880EA21DC0>, <PyQt5.QtWidgets.QLabel object at 0x0000028810BBBF70>, <PyQt5.QtWidgets.QComboBox object at 0x0000028810BB5280>, <PyQt5.QtWidgets.QSplitterHandle object at 0x0000028811D57E50>, <PyQt5.QtWidgets.QScrollBar object at 0x0000028811D57EE0>, <gui.main_widget.TestSystemWidget object at 0x000002880E8FAA60>, <PyQt5.QtWidgets.QWidget object at 0x0000028811D57F70>, <PyQt5.QtWidgets.QScrollBar object at 0x0000028812D8D040>, <PyQt5.QtWidgets.QLabel object at 0x0000028810BB8040>, <PyQt5.QtWidgets.QLabel object at 0x000002880EA218B0>, <PyQt5.QtWidgets.QTableView object at 0x0000028810BBB790>, <PyQt5.QtWidgets.QScrollBar object at 0x0000028812D8D0D0>, <PyQt5.QtWidgets.QScrollBar object at 0x0000028812D8D160>, <PyQt5.QtWidgets.QScrollBar object at 0x0000028812D8D1F0>, <PyQt5.QtWidgets.QScrollBar object at 0x0000028812D8D280>, <PyQt5.QtWidgets.QScrollBar object at 0x0000028812D8D310>, <PyQt5.QtWidgets.QWidget object at 0x0000028812D8D3A0>, <PyQt5.QtWidgets.QLabel object at 0x000002880EA00DC0>, <PyQt5.QtWidgets.QWidget object at 0x0000028812D8D430>, <PyQt5.QtWidgets.QComboBox object at 0x0000028810BB5430>, <gui.file_widget.WgtUser_Profile object at 0x0000028810BB85E0>, <PyQt5.QtWidgets.QLabel object at 0x0000028810BB8AF0>, <PyQt5.QtWidgets.QWidget object at 0x0000028812D8D4C0>, <PyQt5.QtWidgets.QLabel object at 0x0000028810BB5AF0>, <PyQt5.QtWidgets.QPushButton object at 0x000002880EA21790>, <PyQt5.QtWidgets.QWidget object at 0x0000028812D8D550>, <PyQt5.QtWidgets.QPushButton object at 0x000002880EA00820>, <PyQt5.QtWidgets.QWidget object at 0x0000028812D8D5E0>, <PyQt5.QtWidgets.QScrollBar object at 0x0000028812D8D670>, <PyQt5.QtWidgets.QSplitter object at 0x000002887B44D550>, <PyQt5.QtWidgets.QPushButton object at 0x000002880EA00940>, <PyQt5.QtWidgets.QLabel object at 0x0000028810BB51F0>, <PyQt5.QtWidgets.QWidget object at 0x0000028812D8D700>, <PyQt5.QtWidgets.QLabel object at 0x0000028810BB53A0>, <PyQt5.QtWidgets.QScrollBar object at 0x0000028812D8D790>, <PyQt5.QtWidgets.QPushButton object at 0x000002880EA008B0>, <PyQt5.QtWidgets.QFrame object at 0x0000028812D8D820>, <PyQt5.QtWidgets.QWidget object at 0x0000028812D8D8B0>, <PyQt5.QtWidgets.QFrame object at 0x0000028810BBB280>, <PyQt5.QtWidgets.QLineEdit object at 0x00000288130891F0>, <PyQt5.QtWidgets.QLabel object at 0x0000028810BB5C10>, <PyQt5.QtWidgets.QFrame object at 0x0000028810BBB940>, <PyQt5.QtWidgets.QWidget object at 0x0000028812D8D940>, <PyQt5.QtWidgets.QPushButton object at 0x0000028810BB89D0>, <PyQt5.QtWidgets.QLabel object at 0x0000028810BB8EE0>, <PyQt5.QtWidgets.QFrame object at 0x000002880EA00B80>, <PyQt5.QtWidgets.QLabel object at 0x0000028810BB8B80>, <PyQt5.QtWidgets.QPushButton object at 0x000002880EA219D0>, <PyQt5.QtWidgets.QScrollBar object at 0x0000028812D8D9D0>, <PyQt5.QtWidgets.QWidget object at 0x0000028812D8DA60>, <PyQt5.QtWidgets.QPlainTextEdit object at 0x0000028810BB8F70>, <PyQt5.QtWidgets.QLabel object at 0x0000028810BB59D0>, <PyQt5.QtWidgets.QLabel object at 0x0000028810BB5CA0>, <PyQt5.QtWidgets.QPushButton object at 0x000002880EA21CA0>, <PyQt5.QtWidgets.QTableWidget object at 0x000002880EA21820>, <PyQt5.QtWidgets.QLabel object at 0x0000028810BB8280>, <PyQt5.QtWidgets.QPushButton object at 0x0000028810BB8700>, <PyQt5.QtWidgets.QPushButton object at 0x0000028810BBBCA0>, <PyQt5.QtWidgets.QScrollBar object at 0x0000028812D8DAF0>, <PyQt5.QtWidgets.QPushButton object at 0x00000288130894C0>, <PyQt5.QtWidgets.QPushButton object at 0x0000028810BBB430>, <PyQt5.QtWidgets.QScrollBar object at 0x0000028810BB8C10>, <PyQt5.QtWidgets.QCheckBox object at 0x000002880EA21AF0>, <PyQt5.QtWidgets.QPushButton object at 0x0000028810BBBC10>, <PyQt5.QtWidgets.QListView object at 0x0000028812D8DB80>, <PyQt5.QtWidgets.QWidget object at 0x0000028812D8DC10>, <PyQt5.QtWidgets.QLabel object at 0x0000028810BB5EE0>, <PyQt5.QtWidgets.QPushButton object at 0x0000028810BB5700>, <PyQt5.QtWidgets.QWidget object at 0x0000028812D8DCA0>, <PyQt5.QtWidgets.QScrollBar object at 0x0000028812D8DD30>, <PyQt5.QtWidgets.QComboBox object at 0x000002880EA00D30>, <PyQt5.QtWidgets.QComboBox object at 0x0000028810BB8940>, <PyQt5.QtWidgets.QLineEdit object at 0x000002880EA21670>, <PyQt5.QtWidgets.QPushButton object at 0x0000028810BBB8B0>, <PyQt5.QtWidgets.QFrame object at 0x000002880EA211F0>, <PyQt5.QtWidgets.QListView object at 0x0000028812D8DDC0>, <PyQt5.QtWidgets.QLineEdit object at 0x0000028810BB8790>, <gui.widget_testplan.WidgetTestplan object at 0x0000028810BB84C0>, <PyQt5.QtWidgets.QLabel object at 0x0000028810BC10D0>, <PyQt5.QtWidgets.QWidget object at 0x0000028812D8DE50>, <PyQt5.QtWidgets.QLabel object at 0x0000028810BC11F0>, <PyQt5.QtWidgets.QPushButton object at 0x0000028810BC13A0>, <PyQt5.QtWidgets.QLineEdit object at 0x0000028812D8DEE0>, <PyQt5.QtWidgets.QAbstractButton object at 0x0000028812D8DF70>, <PyQt5.QtWidgets.QLineEdit object at 0x000002880EA21B80>, <PyQt5.QtWidgets.QLabel object at 0x0000028810BB5F70>, <PyQt5.QtWidgets.QLabel object at 0x0000028810BB58B0>, <PyQt5.QtWidgets.QLabel object at 0x0000028810BB81F0>, <PyQt5.QtWidgets.QPushButton object at 0x0000028810BC1310>, <PyQt5.QtWidgets.QLineEdit object at 0x00000288130893A0>, <PyQt5.QtWidgets.QWidget object at 0x0000028812D84040>, <PyQt5.QtWidgets.QFrame object at 0x000002880EA21160>, <PyQt5.QtWidgets.QWidget object at 0x0000028812D840D0>, <gui.main_widget.WgtStand object at 0x000002880EA00E50>, <PyQt5.QtWidgets.QWidget object at 0x0000028812D84160>, <PyQt5.QtWidgets.QListView object at 0x0000028812D841F0>, <PyQt5.QtWidgets.QPushButton object at 0x0000028810BC1430>, <PyQt5.QtWidgets.QHeaderView object at 0x0000028812D84280>]]
            meth=[.allWindows]                      value=[[<PyQt5.QtGui.QWindow object at 0x0000028811F158B0>, <PyQt5.QtGui.QWindow object at 0x0000028811F15820>, <PyQt5.QtGui.QWindow object at 0x0000028811F15670>, <PyQt5.QtGui.QWindow object at 0x0000028811F15700>, <PyQt5.QtGui.QWindow object at 0x0000028811F159D0>, <PyQt5.QtGui.QWindow object at 0x0000028811F15A60>]]
            meth=[.applicationDirPath]              value=[C:/Python3810]
            meth=[.applicationDisplayName]          value=[python]
            meth=[.applicationDisplayNameChanged]   value=[<unbound PYQT_SIGNAL applicationDisplayNameChanged()>]
            meth=[.applicationFilePath]             value=[C:/Python3810/python.exe]
            meth=[.applicationName]                 value=[python]
            meth=[.applicationPid]                  value=[17904]
            meth=[.applicationState]                value=[4]
            meth=[.applicationStateChanged]         value=[<unbound PYQT_SIGNAL applicationStateChanged(Qt::ApplicationState)>]
            meth=[.applicationVersion]              value=[3.8.10150.1013]
            meth=[.arguments]                       value=[['C:/!_STARICHENKO-T8/!!!_GD_additional/_PROJECTS/dwdm_test_system/testsystem.pyw']]
            meth=[.autoSipEnabled]                  value=[<built-in function autoSipEnabled>]
            attr=[.beep]                            value=[***MISSED SPECIAL***]
            meth=[.blockSignals]                    value=[<built-in function blockSignals>]
            meth=[.changeOverrideCursor]            value=[<built-in function changeOverrideCursor>]
            meth=[.childEvent]                      value=[<built-in function childEvent>]
            meth=[.children]                        value=[<built-in function children>]
            meth=[.clipboard]                       value=[<PyQt5.QtGui.QClipboard object at 0x0000028813089D30>]
            attr=[.closeAllWindows]                 value=[***MISSED DANGER***]
            meth=[.closingDown]                     value=[False]
            meth=[.colorSpec]                       value=[0]
            meth=[.commitDataRequest]               value=[<unbound PYQT_SIGNAL commitDataRequest(QSessionManager&)>]
            meth=[.connectNotify]                   value=[<built-in function connectNotify>]
            meth=[.cursorFlashTime]                 value=[1060]
            meth=[.customEvent]                     value=[<built-in function customEvent>]
            attr=[.deleteLater]                     value=[***MISSED DANGER***]
            meth=[.desktop]                         value=[<PyQt5.QtWidgets.QDesktopWidget object at 0x0000028813089D30>]
            meth=[.desktopFileName]                 value=[]
            meth=[.desktopSettingsAware]            value=[True]
            meth=[.destroyed]                       value=[<unbound PYQT_SIGNAL destroyed(QObject*)>]
            meth=[.devicePixelRatio]                value=[<built-in function devicePixelRatio>]
            meth=[.disconnect]                      value=[<built-in function disconnect>]
            meth=[.disconnectNotify]                value=[<built-in function disconnectNotify>]
            meth=[.doubleClickInterval]             value=[500]
            meth=[.dumpObjectInfo]                  value=[<built-in function dumpObjectInfo>]
            meth=[.dumpObjectTree]                  value=[<built-in function dumpObjectTree>]
            meth=[.dynamicPropertyNames]            value=[<built-in function dynamicPropertyNames>]
            meth=[.event]                           value=[<built-in function event>]
            meth=[.eventDispatcher]                 value=[<PyQt5.QtCore.QAbstractEventDispatcher object at 0x0000028813089DC0>]
            meth=[.eventFilter]                     value=[<built-in function eventFilter>]
            attr=[.exec]                            value=[***MISSED SPECIAL***]
            attr=[.exec_]                           value=[***MISSED SPECIAL***]
            attr=[.exit]                            value=[***MISSED DANGER***]
            meth=[.findChild]                       value=[<built-in function findChild>]
            meth=[.findChildren]                    value=[<built-in function findChildren>]
            meth=[.flush]                           value=[None]
            meth=[.focusChanged]                    value=[<unbound PYQT_SIGNAL focusChanged(QWidget*,QWidget*)>]
            meth=[.focusObject]                     value=[<PyQt5.QtWidgets.QPushButton object at 0x0000028810BBBCA0>]
            meth=[.focusObjectChanged]              value=[<unbound PYQT_SIGNAL focusObjectChanged(QObject*)>]
            meth=[.focusWidget]                     value=[<PyQt5.QtWidgets.QPushButton object at 0x0000028810BBBCA0>]
            meth=[.focusWindow]                     value=[<PyQt5.QtGui.QWindow object at 0x0000028813089DC0>]
            meth=[.focusWindowChanged]              value=[<unbound PYQT_SIGNAL focusWindowChanged(QWindow*)>]
            meth=[.font]                            value=[<PyQt5.QtGui.QFont object at 0x0000028811F389E0>]
            meth=[.fontChanged]                     value=[<unbound PYQT_SIGNAL fontChanged(QFont)>]
            meth=[.fontDatabaseChanged]             value=[<unbound PYQT_SIGNAL fontDatabaseChanged()>]
            attr=[.fontMetrics]                     value=[***MISSED SPECIAL***]
            meth=[.globalStrut]                     value=[PyQt5.QtCore.QSize()]
            meth=[.hasPendingEvents]                value=[False]
            meth=[.highDpiScaleFactorRoundingPolicy]value=[1]
            meth=[.inherits]                        value=[<built-in function inherits>]
            meth=[.inputMethod]                     value=[<PyQt5.QtGui.QInputMethod object at 0x0000028813089D30>]
            meth=[.installEventFilter]              value=[<built-in function installEventFilter>]
            meth=[.installNativeEventFilter]        value=[<built-in function installNativeEventFilter>]
            meth=[.installTranslator]               value=[<built-in function installTranslator>]
            meth=[.instance]                        value=[<PyQt5.QtWidgets.QApplication object at 0x000002887B44D430>]
            meth=[.isEffectEnabled]                 value=[<built-in function isEffectEnabled>]
            meth=[.isFallbackSessionManagementEnabled]value=[True]
            meth=[.isLeftToRight]                   value=[True]
            meth=[.isQuitLockEnabled]               value=[True]
            meth=[.isRightToLeft]                   value=[False]
            meth=[.isSavingSession]                 value=[<built-in function isSavingSession>]
            meth=[.isSessionRestored]               value=[<built-in function isSessionRestored>]
            meth=[.isSetuidAllowed]                 value=[False]
            meth=[.isSignalConnected]               value=[<built-in function isSignalConnected>]
            meth=[.isWidgetType]                    value=[<built-in function isWidgetType>]
            meth=[.isWindowType]                    value=[<built-in function isWindowType>]
            meth=[.keyboardInputInterval]           value=[400]
            meth=[.keyboardModifiers]               value=[<PyQt5.QtCore.Qt.KeyboardModifiers object at 0x0000028811F389E0>]
            meth=[.killTimer]                       value=[<built-in function killTimer>]
            meth=[.lastWindowClosed]                value=[<unbound PYQT_SIGNAL lastWindowClosed()>]
            meth=[.layoutDirection]                 value=[0]
            meth=[.layoutDirectionChanged]          value=[<unbound PYQT_SIGNAL layoutDirectionChanged(Qt::LayoutDirection)>]
            meth=[.libraryPaths]                    value=[['C:/Python3810/lib/site-packages/PyQt5/Qt5/plugins', 'C:/Python3810']]
            meth=[.metaObject]                      value=[<built-in function metaObject>]
            meth=[.modalWindow]                     value=[None]
            meth=[.mouseButtons]                    value=[<PyQt5.QtCore.Qt.MouseButtons object at 0x0000028811F38970>]
            attr=[.moveToThread]                    value=[***MISSED DANGER***]
            meth=[.notify]                          value=[<built-in function notify>]
            meth=[.objectName]                      value=[<built-in function objectName>]
            meth=[.objectNameChanged]               value=[<unbound PYQT_SIGNAL objectNameChanged(QString)>]
            meth=[.organizationDomain]              value=[]
            meth=[.organizationName]                value=[]
            meth=[.overrideCursor]                  value=[None]
            meth=[.palette]                         value=[<PyQt5.QtGui.QPalette object at 0x0000028811F38970>]
            meth=[.paletteChanged]                  value=[<unbound PYQT_SIGNAL paletteChanged(QPalette)>]
            meth=[.parent]                          value=[<built-in function parent>]
            meth=[.platformName]                    value=[windows]
            meth=[.postEvent]                       value=[<built-in function postEvent>]
            meth=[.primaryScreen]                   value=[<PyQt5.QtGui.QScreen object at 0x0000028813089DC0>]
            meth=[.primaryScreenChanged]            value=[<unbound PYQT_SIGNAL primaryScreenChanged(QScreen*)>]
            meth=[.processEvents]                   value=[None]
            meth=[.property]                        value=[<built-in function property>]
            attr=[.pyqtConfigure]                   value=[***MISSED SPECIAL***]
            meth=[.queryKeyboardModifiers]          value=[<PyQt5.QtCore.Qt.KeyboardModifiers object at 0x0000028811F38890>]
            meth=[.quit]                            value=[None]
            meth=[.quitOnLastWindowClosed]          value=[True]
            meth=[.receivers]                       value=[<built-in function receivers>]
            attr=[.removeEventFilter]               value=[***MISSED DANGER***]
            attr=[.removeLibraryPath]               value=[***MISSED DANGER***]
            attr=[.removeNativeEventFilter]         value=[***MISSED DANGER***]
            attr=[.removePostedEvents]              value=[***MISSED DANGER***]
            attr=[.removeTranslator]                value=[***MISSED DANGER***]
            meth=[.restoreOverrideCursor]           value=[None]
            meth=[.saveStateRequest]                value=[<unbound PYQT_SIGNAL saveStateRequest(QSessionManager&)>]
            meth=[.screenAdded]                     value=[<unbound PYQT_SIGNAL screenAdded(QScreen*)>]
            meth=[.screenAt]                        value=[<built-in function screenAt>]
            attr=[.screenRemoved]                   value=[***MISSED DANGER***]
            meth=[.screens]                         value=[[<PyQt5.QtGui.QScreen object at 0x000002880EA21430>, <PyQt5.QtGui.QScreen object at 0x000002880EA210D0>]]
            meth=[.sendEvent]                       value=[<built-in function sendEvent>]
            meth=[.sendPostedEvents]                value=[None]
            meth=[.sender]                          value=[<built-in function sender>]
            meth=[.senderSignalIndex]               value=[<built-in function senderSignalIndex>]
            meth=[.sessionId]                       value=[<built-in function sessionId>]
            meth=[.sessionKey]                      value=[<built-in function sessionKey>]
            attr=[.setActiveWindow]                 value=[***MISSED DANGER***]
            attr=[.setApplicationDisplayName]       value=[***MISSED DANGER***]
            attr=[.setApplicationName]              value=[***MISSED DANGER***]
            attr=[.setApplicationVersion]           value=[***MISSED DANGER***]
            attr=[.setAttribute]                    value=[***MISSED DANGER***]
            attr=[.setAutoSipEnabled]               value=[***MISSED DANGER***]
            attr=[.setColorSpec]                    value=[***MISSED DANGER***]
            attr=[.setCursorFlashTime]              value=[***MISSED DANGER***]
            attr=[.setDesktopFileName]              value=[***MISSED DANGER***]
            attr=[.setDesktopSettingsAware]         value=[***MISSED DANGER***]
            attr=[.setDoubleClickInterval]          value=[***MISSED DANGER***]
            attr=[.setEffectEnabled]                value=[***MISSED DANGER***]
            attr=[.setEventDispatcher]              value=[***MISSED DANGER***]
            attr=[.setFallbackSessionManagementEnabled]value=[***MISSED DANGER***]
            attr=[.setFont]                         value=[***MISSED DANGER***]
            attr=[.setGlobalStrut]                  value=[***MISSED DANGER***]
            attr=[.setHighDpiScaleFactorRoundingPolicy]value=[***MISSED DANGER***]
            attr=[.setKeyboardInputInterval]        value=[***MISSED DANGER***]
            attr=[.setLayoutDirection]              value=[***MISSED DANGER***]
            attr=[.setLibraryPaths]                 value=[***MISSED DANGER***]
            attr=[.setObjectName]                   value=[***MISSED DANGER***]
            attr=[.setOrganizationDomain]           value=[***MISSED DANGER***]
            attr=[.setOrganizationName]             value=[***MISSED DANGER***]
            attr=[.setOverrideCursor]               value=[***MISSED DANGER***]
            attr=[.setPalette]                      value=[***MISSED DANGER***]
            attr=[.setParent]                       value=[***MISSED DANGER***]
            attr=[.setProperty]                     value=[***MISSED DANGER***]
            attr=[.setQuitLockEnabled]              value=[***MISSED DANGER***]
            attr=[.setQuitOnLastWindowClosed]       value=[***MISSED DANGER***]
            attr=[.setSetuidAllowed]                value=[***MISSED DANGER***]
            attr=[.setStartDragDistance]            value=[***MISSED DANGER***]
            attr=[.setStartDragTime]                value=[***MISSED DANGER***]
            attr=[.setStyle]                        value=[***MISSED DANGER***]
            attr=[.setStyleSheet]                   value=[***MISSED DANGER***]
            attr=[.setWheelScrollLines]             value=[***MISSED DANGER***]
            attr=[.setWindowIcon]                   value=[***MISSED DANGER***]
            meth=[.signalsBlocked]                  value=[<built-in function signalsBlocked>]
            meth=[.startDragDistance]               value=[10]
            meth=[.startDragTime]                   value=[500]
            meth=[.startTimer]                      value=[<built-in function startTimer>]
            meth=[.startingUp]                      value=[False]
            obj=[.staticMetaObject]                 value=[<PyQt5.QtCore.QMetaObject object at 0x0000028811F389E0>]
            meth=[.style]                           value=[<PyQt5.QtWidgets.QCommonStyle object at 0x0000028810BB5EE0>]
            meth=[.styleHints]                      value=[<PyQt5.QtGui.QStyleHints object at 0x0000028810BB5EE0>]
            meth=[.styleSheet]                      value=[<built-in function styleSheet>]
            meth=[.sync]                            value=[None]
            meth=[.testAttribute]                   value=[<built-in function testAttribute>]
            meth=[.thread]                          value=[<built-in function thread>]
            meth=[.timerEvent]                      value=[<built-in function timerEvent>]
            meth=[.topLevelAt]                      value=[<built-in function topLevelAt>]
            meth=[.topLevelWidgets]                 value=[[<PyQt5.QtWidgets.QFrame object at 0x0000028810BBB940>, <PyQt5.QtWidgets.QWidget object at 0x0000028810BB5EE0>, <PyQt5.QtWidgets.QPushButton object at 0x0000028810BBB9D0>, <PyQt5.QtWidgets.QFrame object at 0x0000028810BBBB80>, <PyQt5.QtWidgets.QLabel object at 0x0000028810BB5DC0>, <PyQt5.QtWidgets.QPushButton object at 0x0000028810BBBA60>, <gui.authorization_widget.WidgetServerAuthorization object at 0x000002881306CF70>]]
            meth=[.topLevelWindows]                 value=[[<PyQt5.QtGui.QWindow object at 0x0000028810BB5EE0>, <PyQt5.QtGui.QWindow object at 0x0000028810BB5DC0>]]
            meth=[.tr]                              value=[<built-in function tr>]
            meth=[.translate]                       value=[<built-in function translate>]
            meth=[.wheelScrollLines]                value=[3]
            meth=[.widgetAt]                        value=[<built-in function widgetAt>]
            meth=[.windowIcon]                      value=[<PyQt5.QtGui.QIcon object at 0x0000028810BB5EE0>]
            ////////////////////////////////////////////////////////////////////////////////////////////////////

            Process finished with exit code -1073740940 (0xC0000374)
        """
        top_level_widgets = QApplication.topLevelWidgets()
        if not top_level_widgets:
            self.app = QApplication([])
            # QApplication.setQuitOnLastWindowClosed(False)     # dont help!

        # elif top_level_widgets and not QApplication.hasPendingEvents():
        #     msg = f"DETECTED START [{self.__class__.__name__=}] NOT IN MAIN THREAD!!!"
        #     UFU.logging_and_print_debug(msg)
        #     # raise Exception(msg)
        #     # QApplication.applicationName() - on child thread will show not blank!!!
        #     # QApplication.hasPendingEvents() - on child thread will show False!!!
        #     # for wgt_i in top_level_widgets:
        #     #     print(f"{wgt_i=}\t{type(wgt_i)=}\t{wgt_i.objectName()=}\t{wgt_i.accessibleName()=}")
        #
        #     # for wgt_i in top_level_widgets:
        #     #         __class__.WGT_ROOT = wgt_i.dialog_obj
        #
        #     if __class__.WGT_ROOT is not None:
        #         msg = f"EXISTS WGT_ROOT!!!"
        #         UFU.logging_and_print_warning(msg)
        #     else:
        #         msg = f"NOT FOUND WGT_ROOT!!!"
        #         UFU.logging_and_print_warning(msg)

    # =================================================================================================================
    @classmethod
    def last_answer_set(cls, result):
        cls.ANSWER_LAST = result
        cls.ANSWER_READY = True

    # SIMPLE ----------------------------------------------------------------------------------------------------------
    def _only_simple_0_nolock_noanswer(self, msg: Union[str, list[str]] = "msg", title: str = "title"):
        if isinstance(msg, (list, tuple)):   # msg
            msg = '\n'.join(msg)

        wgt = QFrame()
        wgt.setWindowFlags(Qt.ToolTip)

        wgt.setWindowTitle(title)
        wgt.setStyleSheet(f"background: rgb{COLOR_TUPLE_RGB.LIGHT_YELLOW}")
        wgt.setFrameStyle(3)
        wgt.setLineWidth(5)
        wgt.setMinimumWidth(300)
        wgt.setMinimumHeight(100)

        lbl = QLabel(msg)

        btn_1 = QPushButton("прочитано")
        btn_1.setStyleSheet("background: rgb(255,255,50)")
        btn_1.clicked.connect(wgt.close)

        layout = QVBoxLayout()
        layout.addWidget(lbl)
        layout.addWidget(btn_1)
        wgt.setLayout(layout)

        __class__.WGT_NOLOCK_NOANSWER = wgt
        __class__.WGT_NOLOCK_NOANSWER.show()

    def _only_simple_1_info(self, msg="msg", title="title"):
        answer = QMessageBox.information(self, title, msg, QMessageBox.Yes | QMessageBox.No)
        result = answer in [QMessageBox.Yes, 0]       # 0 если ACCEPTED! like wgt_i.accept()
        # UFU.logging_and_print_info(f"{answer=}")
        self.last_answer_set(result)
        return result

    def _only_simple_2_question(self, msg="msg", title="title"):
        answer = QMessageBox.question(self, title, msg, QMessageBox.Yes | QMessageBox.No)
        result = answer in [QMessageBox.Yes, 0]
        self.last_answer_set(result)
        return result

    def _only_simple_22_warning(self, msg="msg", title="title"):
        pass

    def _only_simple_3_critical(self, msg="msg", title="title"):
        answer = QMessageBox.critical(self, title, msg, QMessageBox.Yes | QMessageBox.No)
        result = answer in [QMessageBox.Yes, 0]
        self.last_answer_set(result)
        return result

    # INPUT -----------------------------------------------------------------------------------------------------------
    def _only_input_string(self, msg="Input string:", title="InputDialog"):
        result = None
        text, ok = QInputDialog.getText(self, title, msg)

        if ok and text:
            result = text

        self.last_answer_set(result)
        return result

    # SELECTORS -------------------------------------------------------------------------------------------------------
    def _only_select_file(self, title="SelectFile", path=''):
        """
        :param path:
            ""      - __file__
            "/"     - C:/
            ".."    - __file__/../
        """
        file_name = QFileDialog.getOpenFileName(self, title, path)[0]
        result = file_name or None

        self.last_answer_set(result)
        return result

    def _only_select_font(self, *args, **kwargs):
        # todo: finish!!!!
        result = None
        font_obj, ok = QFontDialog.getFont()
        if ok:
            result = str(font_obj)

        self.last_answer_set(result)
        return result

    def _only_select_color(self, *args, **kwargs):
        result = None
        color_obj = QColorDialog.getColor()
        if color_obj.isValid():
            result = color_obj.name()

        self.last_answer_set(result)
        return result

    # EXTENDED ========================================================================================================
    def _extended_thread_save_dialog(
            self,
            param1="msg",   # "msg"
            param2=None,      # title or path!
            _type=1,
            return_always_true=False,

            ask_only_if=True,
            func_link_do_while=None,

            autoaccept_tracking_value_link=None,
            autoaccept_link=None,
            timeout=0):
        """
        makes all dialogs thread safe!!!

        Получает ответ оператора - выдает True, если нажали OK иначе False.
        RECOMMENDED: use all parameters as KWARGS!!!

        :param ask_only_if: глобальный вопрос - показывать или нет окно вопроса - если нет то результатом функции будет True чтобы не мешать дальнейшим процессам!!!
        :param func_link_do_while: если указана - перед отображением окна она проверяется и окно протолжает отображаться то тех пор пока не будет изменено значение на False!
            или нажата кнопка NO - РАБОТАЕТ!!!
        :param return_always_true: создана для случая когда нам не важен ответ, но и нежелательно выдавать False! всегда будет выдавать True

        :param autoaccept_tracking_value_link: функция, если указана, если указано, то в окно вместе с сообщением выводится полученое значение (и обновляется с прохождением autoaccept_link)
        :param autoaccept_link: функция, если указана, то проверяется c периодичностью, если получила результат True - то считается что нажата кнопка OK, окно закрывается!
        :param timeout: время в секундах - если задана функция autoaccept_link, то она проверяется именно с этим промежутком времени

        How to use text formatting in gui ask:
            <br><br> - brake line
            <b>ПРЕДУПРЕЖДЕНИЕ</b> - Bold
            <font size=20 color=red></font> - font size/ color not worked!
        """
        # INIT RESULTS ------------------------------------------------------------------------------------------------
        __class__.ANSWER_READY = None
        __class__.ANSWER_LAST = None
        __class__.ANSWER_LAST_WAS_AUTOACCEPTED = None

        # -------------------------------------------------------------------------------------------------------------
        # INPUT
        if isinstance(param1, (list, tuple)):   # msg
            param1 = '\n'.join(param1)

        if func_link_do_while is None:
            func_link_do_while = LAMBDA_TRUE
        elif not callable(func_link_do_while):
            msg = f"получено неверное значение для [{func_link_do_while=}]"
            print(msg)
            raise Exception(msg)

        # -------------------------------------------------------------------------------------------------------------
        if __class__.WGT_ROOT is None:
            if _type == 0:
                emit_link = self.s_type0.emit
            elif _type == 1:
                emit_link = self.s_type1.emit
            elif _type == 2:
                emit_link = self.s_type2.emit
            elif _type == 3:
                emit_link = self.s_type3.emit
            elif _type == 4:
                emit_link = self.s_type4.emit
            elif _type == 5:
                emit_link = self.s_type5.emit
            elif _type == 6:
                emit_link = self.s_type6.emit
            elif _type == 7:
                emit_link = self.s_type7.emit

        else:
            if _type == 0:
                emit_link = __class__.WGT_ROOT.s_type0.emit
            elif _type == 1:
                emit_link = __class__.WGT_ROOT.s_type1.emit
            elif _type == 2:
                emit_link = __class__.WGT_ROOT.s_type2.emit
            elif _type == 3:
                emit_link = __class__.WGT_ROOT.s_type3.emit
            elif _type == 4:
                emit_link = __class__.WGT_ROOT.s_type4.emit
            elif _type == 5:
                emit_link = __class__.WGT_ROOT.s_type5.emit
            elif _type == 6:
                emit_link = __class__.WGT_ROOT.s_type6.emit
            elif _type == 7:
                emit_link = __class__.WGT_ROOT.s_type7.emit

        # -------------------------------------------------------------------------------------------------------------
        result = False
        if ask_only_if:
            time_start = time.time()
            while func_link_do_while():
                # timeout ------------------------------------------------------------------------
                if timeout and time.time() - time_start > timeout:
                    break

                # start thread to close Dialog!!! ------------------------------------------------
                if autoaccept_link is not None:
                    self.autoaccept_start_thread(autoaccept_link)

                # start Dialog!!! ------------------------------------------------
                emit_link(param1, param2)

                if _type == 0:
                    break

                while True:
                    print(f"ожидание ответа пользователя [{autoaccept_link=}/{__class__.ANSWER_LAST_WAS_AUTOACCEPTED=}]")
                    if __class__.ANSWER_READY:
                        result = __class__.ANSWER_LAST
                        break
                    elif __class__.ANSWER_LAST_WAS_AUTOACCEPTED:
                        result = True
                        break
                    time.sleep(1)

                _msg = f"Интерактивный ответ пользователя [{result=}/{param1=}/{param2=}]"
                print(_msg, result)

                if not result or func_link_do_while == LAMBDA_TRUE:
                    break

                time.sleep(0.5)

        if return_always_true:
            result = True
        return result

    # SIMPLE ----------------------------------------------------------------------------------------------------------
    def simple_0_nolock_noanswer(self, *args, **kwargs):
        return self._extended_thread_save_dialog(*args, _type=0, **kwargs)

    def simple_1_info(self, *args, **kwargs):
        return self._extended_thread_save_dialog(*args, _type=1, **kwargs)

    def simple_2_question(self, *args, **kwargs):
        return self._extended_thread_save_dialog(*args, _type=2, **kwargs)

    def simple_3_critical(self, *args, **kwargs):
        return self._extended_thread_save_dialog(*args, _type=3, **kwargs)

    # INPUT -----------------------------------------------------------------------------------------------------------
    def input_string(self, *args, **kwargs):
        return self._extended_thread_save_dialog(*args, _type=4, **kwargs)

    # SELECTORS -------------------------------------------------------------------------------------------------------
    def select_file(self, *args, **kwargs):
        return self._extended_thread_save_dialog(*args, _type=5, **kwargs)

    def select_font(self, *args, **kwargs):
        return self._extended_thread_save_dialog(*args, _type=6, **kwargs)

    def select_color(self, *args, **kwargs):
        return self._extended_thread_save_dialog(*args, _type=7, **kwargs)

    # COMPOSITION =====================================================================================================
    def _composed_box(self, msg="button_box?", title="button_box"):
        """
        composed msg box by wgts!
        if you need simple ask YesNo - use other simple from the beginning!
        """
        qdialog = QDialog()

        layout = QVBoxLayout(qdialog)
        layout.addWidget(QLabel(msg))

        buttons = QDialogButtonBox(qdialog)
        buttons.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        # buttons.setOrientation(Qt.Horizontal)
        layout.addWidget(buttons)

        qdialog.setWindowTitle(title)

        buttons.accepted.connect(qdialog.accept)
        buttons.rejected.connect(qdialog.reject)
        qdialog.exec_()
        result = qdialog.result() == 1    # 0=Cancel, 1=OK
        self.last_answer_set(result)
        return result

    # =================================================================================================================
    def _QDialog(self):
        qdialog = QDialog()
        qdialog.exec_()

    def _test_some(self):
        self.simple_1_info("hello1")
        self.simple_2_question("hello2")
        self.simple_3_critical("hello3")
        self.input_string("hello4")
        self.select_file("hello5")
        self.select_font("hello6")
        self.select_color("hello7")


# =====================================================================================================================
INSTRUCTION_HTML = """
    <html>
    #########################################################################
    <h1>ИНСТРУКЦИЯ ПО ТЕСТИРОВАНИЮ BACKPLANE (ШАССИ КРЕЙТА)</h1>
    
    <h2>1. В ШАССИ УСТАНОВИТЕ ВСЕ УСТРОЙСТВА!</h2>
    <p>
    - Не должно быть ни одного свободного места (все PS, все CU и FU должны быть заняты)<br>
    </p>
    
    <h2>2. CU</h2>
    <p>
    - могут быть разными, но должна быть одинаковая версия ATLAS!<br>
    - Версия Atlas должна быть не ниже 2.3.5 (иначе будут ошибки проверки ETHERNET)<br>
    - Запуск необходимо производить с CU0, а не с CU1<br>
    (иначе будут ошибки в определении подключенных устройств)<br>
    </p>
    
    <h2>3. устройства В8</h2>
    <p>
    - во все слоты B8 установите КАМА не ниже v1.1<br>
    - если будут отказы на КАМА, то попробуйте ревизию плат v1.3<br>
    - если использовать НЕ КАМА, то могут не пройти тесты ETHERNET!<br>
    - если использовать ПАССИВНЫЕ УСТРОЙСТВА, то не пройдут тесты UART и ETHERNET!<br>
    </p>
    
    <h2>4. БЛОКИ ПИТАНИЯ</h2>
    <p>
    - могут быть любые разные (даже AC/DC)<br>
    - Подайте питание на оба блока питания<br>
    </p>
    
    <h2>5. Запустите АвтоТестирование и следуйте указаниям</h2>
    
    <h3>ПРИМЕЧАНИЕ:</h3>
    <p>
    - если будут ошибки когда их очевидно не должно быть - перезапустите VOLGA!
    </p>
    
    <p>
    <b>YES/NO</b>=Прочинано - продолжить работу
    </p>
    
    </html>
"""


def try__autoaccept():
    GuiDialog().simple_1_info(INSTRUCTION_HTML, autoaccept_link=SLEEP_TRUE)
    GuiDialog().simple_1_info(INSTRUCTION_HTML, autoaccept_link=SLEEP_TRUE)


def try__GuiDialog():
    GuiDialog().simple_1_info(INSTRUCTION_HTML)
    GuiDialog().simple_2_question('<h1>hel\nlo</h1><b>12345<br>1234</b> 21211212 <br>')
    GuiDialog().simple_3_critical()
    GuiDialog().input_string()
    GuiDialog().select_file()
    GuiDialog().select_font()
    GuiDialog().select_color()
    GuiDialog()._composed_box()
    GuiDialog()._QDialog()
    GuiDialog().simple_1_info(INSTRUCTION_HTML)


def try__static():
    print(GuiDialog().simple_1_info(INSTRUCTION_HTML))
    print(GuiDialog().simple_1_info(INSTRUCTION_HTML))


# =====================================================================================================================
if __name__ == '__main__':
    try__info()
    # try__autoaccept()
    # print(GuiDialog().simple_1_info('<h1>hel\nlo</h1><b>12345<br>1234</b> 21211212 <br>'))
    # print(GuiDialog().simple_1_info('<h1>hel\nlo</h1><b>12345<br>1234</b> 21211212 <br>'))


# =====================================================================================================================
