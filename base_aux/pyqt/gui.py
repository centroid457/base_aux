import time
from typing import *
import sys
import pathlib

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from .base import Row_, Dev_, Data_
from .tm import TableModelTemplate
from .th import HeaderViewCB
from .hl import *


# =====================================================================================================================
TYPE__SIZE_TUPLE = tuple[Optional[int], Optional[int]]


class Dialogs:
    """
    attempt to keep all  available dialogs in one place!
    so to be sure there are no any other available!
    """
    @staticmethod
    def info__about() -> None:
        QMessageBox.information(
            None,
            'О программе',
            (
                'ООО Элемент-Инжиниринг,\n'
                'Программа проведения тестирования блоков питания\n'
                '(стендовые испытания ОТК)'
             )
        )


# =====================================================================================================================
class Gui(QMainWindow):     # QWidget/QMainWindow
    DATA: Optional[Any] = None

    # SETTINGS --------------------------------------------------
    START: bool = True

    TITLE: str = "[GUI] Template"
    LOGO: str = "logo.jpg"
    CENTER: bool = True

    SIZE_MINIMUM: TYPE__SIZE_TUPLE = (None, None)
    SIZE_MAXIMUM: TYPE__SIZE_TUPLE = (None, None)
    SIZE_FIXED: TYPE__SIZE_TUPLE = (None, None)
    SIZE: TYPE__SIZE_TUPLE = (None, None)
    MOVE: TYPE__SIZE_TUPLE = (None, None)

    FLAGS: dict[int, str] = {
        # TODO: use separated as CLASS!!! with special FLAG methods!!! sum/del/check/... and try to mark as True/False/None

        # UNCOMMENT IF NEEDED!
        # values are just for information!
        # if some flags overlays/conflict - used last activated

        # BORDER/FRAME/TITLE ------------------------------------------------------------------
        # Qt.FramelessWindowHint: "[frame]hide outer frame/border (with title), to tern back title add WindowTitleHint",
        # Qt.WindowTitleHint: "[title]force turn on (after FramelessWindowHint) window title",
        # Qt.CustomizeWindowHint: "[title]hide std frame border with title",

        # GEOMETRY ----------------------------------------------------------------------------
        # Qt.MSWindowsFixedSizeDialogHint: "[geometry]block window mouse resizing",

        # BTNS --------------------------------------------------------------------------------
        # Qt.WindowSystemMenuHint: "???[btn]deactivate all btns",
        # Qt.WindowMinimizeButtonHint: "[btn]activate ONLY MINimize",
        # Qt.WindowMaximizeButtonHint: "[btn]activate ONLY MAXimize",
        # Qt.WindowMinMaxButtonsHint: "[btn]activate ONLY MAX+MINimize",
        # Qt.WindowCloseButtonHint: "[btn]keep only CLOSE",
        # Qt.WindowContextHelpButtonHint: "[btn]keep only HELP +CLOSE(but inactivated) = почемуто нельзя обьединить с чемто еще!!!",

        # LAYERS -------------------------------------------------------------------------------
        # Qt.WindowStaysOnTopHint: "[layer] always on TOP",
        # Qt.WindowStaysOnBottomHint: "[layer] always on BOTTOM",
    }

    # AUXILIARY --------------------------------------------------
    _QAPP: QApplication = QApplication([])

    # COMMON ------------------------------------------------------
    DIALOGS: type[Dialogs] = Dialogs

    MENU: Optional[QMenu] = None
    SB: Optional[QStatusBar] = None
    CENTRAL_WGT: QWidget = None
    LAYOUT_MAIN: QLayout = None

    BTN: Optional[QPushButton] = None
    CB: Optional[QCheckBox] = None
    TV: Optional[QTableView] = None
    TM: Optional[QAbstractTableModel] = None
    PTE: Optional[QPlainTextEdit] = None
    HL: Optional[QSyntaxHighlighter] = None
    HL_STYLES: Optional[HlStyles] = None

    def __init__(self, data: Optional[Any] = None):
        super().__init__()

        if data is not None:
            self.DATA = data

        if self.START:
            self.run()

    def run(self):
        self.main_window_prepare()
        self.wgt_create()
        self.slots_connect()

        # GUI SHOW ----------------------------------------------------------------------------------------------------
        self._wgt_main__apply_settings()
        self.show()
        if self.CENTER:
            self._wgt_main__center()

        # starting PYQT in thread - NOT AVAILABLE!!! ---------------------------
        # i tried switch all even show() into it - not working!
        # thread = threading.Thread(target=self.run)
        # thread.start()
        # thread.join()

        exit_code = self._QAPP.exec()
        # time.sleep(5)
        if exit_code == 0:
            print(f"[OK]GUI({exit_code=})closed correctly")
        else:
            print(f"[FAIL]GUI({exit_code=})closed INCORRECTLY")
        sys.exit(exit_code)

    # MAIN WINDOW =====================================================================================================
    def _wgt_main__apply_settings(self) -> None:
        # TITLE --------------------------------------------------
        self.setWindowTitle(self.TITLE)
        self._wgt_main__apply_logo()

        # FLAGS ---------------------------------------------------
        flag_cum = 0
        for flag in self.FLAGS:
            flag_cum |= flag
        if flag_cum:
            self.setWindowFlags(flag_cum)

        # GEOMETRY ------------------------------------------------
        if self.SIZE_MINIMUM[0]:
            self.setMinimumWidth(self.SIZE_MINIMUM[0])
        if self.SIZE_MINIMUM[1]:
            self.setMinimumHeight(self.SIZE_MINIMUM[1])

        if self.SIZE_MAXIMUM[0]:
            self.setMaximumWidth(self.SIZE_MAXIMUM[0])
        if self.SIZE_MAXIMUM[1]:
            self.setMaximumHeight(self.SIZE_MAXIMUM[1])

        if self.SIZE_FIXED[0]:
            self.setFixedWidth(self.SIZE_FIXED[0])
        if self.SIZE_FIXED[1]:
            self.setFixedHeight(self.SIZE_FIXED[1])

        if self.SIZE[0] or self.SIZE[1]:
            width = self.SIZE[0] or self.width()
            height = self.SIZE[1] or self.height()
            self.resize(width, height)

        if self.MOVE[0] or self.MOVE[1]:
            x = self.MOVE[0] or self.x()
            y = self.MOVE[1] or self.y()
            self.move(x, y)

        # USER ------------------------------------------------

    def _wgt_main__apply_logo(self) -> None:
        """
        need square size for logo!
        """
        logo_filepath = pathlib.Path(self.LOGO)
        if logo_filepath.is_file() and logo_filepath.exists():
            self._QAPP.setWindowIcon(QIcon(logo_filepath.name))

            try:
                # turn on logo for python-applications (only for Windows) as associations
                from PyQt5.QtWinExtras import QtWin
                QtWin.setCurrentProcessExplicitAppUserModelID('mycompany.myproduct.subproduct.version')
            except:
                pass

    def _wgt_main__center(self):
        """
        center the main window considering MULTY MONITORS.
        NOTE: work incorrect in INIT!!! use in root module right after wgt.SHOW() not before!!!
        """
        window_geometry = self.frameGeometry()
        # print(f"window_geometry={window_geometry}")      # PyQt5.QtCore.QRect(100, 100, 500, 500)

        display_obj = QApplication.desktop()
        # print(f"display_obj={display_obj}")      # <PyQt5.QtWidgets.QDesktopWidget object at 0x0000020630E771F0>

        display_index = display_obj.screenNumber(display_obj.cursor().pos())
        # print(f"display_index={display_index}")    # 1

        display_geometry = display_obj.screenGeometry(display_index)
        # print(f"display_geometry={display_geometry}")    # PyQt5.QtCore.QRect(1366, 0, 1920, 1080)

        display_central_point = display_geometry.center()
        # print(f"display_central_point={display_central_point}")    # PyQt5.QtCore.QPoint(2325, 539)

        self.move(
            display_central_point.x() - window_geometry.width()//2,
            display_central_point.y() - window_geometry.height()//2
        )

    # WINDOW ==========================================================================================================
    def main_window_prepare(self) -> None:
        self.CENTRAL_WGT = QWidget()
        self.setCentralWidget(self.CENTRAL_WGT)

        self.MENU_create()
        self.SB_create()

    def wgt_create(self) -> None:
        self.BTN_create()
        self.CB_create()
        self.TV_create()
        self.PTE_create()
        self.HL_create()
        self.BTNS_PTE_create()

        # GRID --------------------------------------------------------------------------------------------------------
        layout_grid = QGridLayout()

        # settings -----------------------------------
        layout_grid.setColumnStretch(1, 2)
        layout_grid.setRowStretch(2, 2)

        layout_grid.setHorizontalSpacing(2)
        layout_grid.setVerticalSpacing(1)
        layout_grid.setSpacing(1)

        layout_grid.setColumnMinimumWidth(0, 100)
        layout_grid.setRowMinimumHeight(1, 50)

        # wgts ---------------------------------------
        layout_grid.addWidget(QLabel("00"), 0, 0)
        layout_grid.addWidget(QLabel("01"), 0, 1)
        layout_grid.addWidget(QLabel("02"), 0, 2)
        layout_grid.addWidget(QLabel("03"), 0, 3)

        layout_grid.addWidget(QLabel("10"), 1, 0)
        layout_grid.addWidget(QLabel("11-12"), 1, 1, 1, 2)
        layout_grid.addWidget(QLabel("13"), 1, 3)

        layout_grid.addWidget(QLabel("20"), 2, 0)
        layout_grid.addWidget(QLabel("21-end"), 2, 1, 2, -1)

        # pte_btns -------------------------------------------------------------------------------------------
        # wgts --------------------------------------
        # TODO: FINISH WITH BTNS_BLOCK!!!!

        # layout ------------------------------------
        # layout_h = QHBoxLayout()
        # layout_h.addWidget(self.)

        # LAYOUT_MAIN -------------------------------------------------------------------------------------------------
        layout_v = QVBoxLayout()
        layout_v.addLayout(layout_grid)
        layout_v.addWidget(self.CB)
        layout_v.addWidget(self.BTN)
        # layout_v.addLayout(layout_h)
        layout_v.addWidget(self.PTE)

        # LAYOUT_MAIN -------------------------------------------------------------------------------------------------
        self.LAYOUT_MAIN = QHBoxLayout()
        self.LAYOUT_MAIN.addWidget(self.TV)
        self.LAYOUT_MAIN.addLayout(layout_v)

        self.CENTRAL_WGT.setLayout(self.LAYOUT_MAIN)

    # MAINWINDOW ======================================================================================================
    def MENU_create(self) -> None:
        """
        '&'sign
        -------
        1. is for ALT+ running!
        2. if exists several same links - it would be switched by circle

        CONSTRAINTS
        -----------
        1. could create ONLY for QMainWindow! not for just a QWidget!

        TODO: add folder select + change title for it name
            https://www.pythontutorial.net/pyqt/pyqt-qstatusbar/
        """
        if isinstance(self, QMainWindow):
            self.MENU = self.menuBar()
        elif isinstance(self, QWidget):
            # this is just for future!
            # self.MENU = QMenuBar()
            pass

        # menu_file = self.MENU.addMenu('&File')
        # menu_edit = self.MENU.addMenu('&Edit')
        menu_help = self.MENU.addMenu('&Справка')

        about_action = QAction('O приложении', self)      # if no fileIcon exists - no error/warn!
        # about_action.setStatusTip('O приложении')
        about_action.setShortcut('F1')
        about_action.triggered.connect(Dialogs.info__about)
        menu_help.addAction(about_action)

    def SB_create(self) -> None:
        self.SB = self.statusBar()
        self.SB.showMessage('Ready', 3000)

        # lbl_1 = QLabel("lbl: 0")
        # lbl_date = QLabel("Date: ...")
        self.SB.addPermanentWidget(QLabel("..."))
        # self.SB.addPermanentWidget(lbl_1)
        # self.SB.addPermanentWidget(lbl_date)

        # lbl_date.setText(f'Date: {time.time()}')

    # WGTS ============================================================================================================
    def BTN_create(self) -> None:
        self.BTN = QPushButton("BTN")

        # SETTINGS -------------------------
        self.BTN.setText("BTN_mod")
        self.BTN.setToolTip("ToolTip")

        self.BTN.setCheckable(True)
        # self.BTN.setChecked(False)
        # self.BTN.setFlat(True)        # виджет вида Label!!! НО нажатия визуализирует как виджет BTN!!!
        # self.BTN.setDefault(True)     # кажется выделяет рамкой навсегда среди всех?

        # self.BTN.setEnabled(True)
        # self.BTN.setDisabled(True)
        # self.BTN.setVisible(True)
        # self.BTN.setHidden(True)

        # GEOMETRY ----------------------
        # self.BTN.setContentsMargins(1000, 1000, 1000, 1000)     # ничего не дает!!!
        # self.BTN.setSizeIncrement(100, 100)     # не понял!!!

        # self.BTN.setMinimumWidth(5)
        # self.BTN.setMinimumHeight(5)
        # self.BTN.setMinimumSize(5, 5)

        # self.BTN.setMaximumWidth(300)
        # self.BTN.setMaximumHeight(20)
        # self.BTN.setMaximumSize(300, 20)

        # если это сделать, то расширяться не будет!!!!!
        # self.BTN.setFixedWidth(100)      # in pixels
        # self.BTN.setFixedHeight(20)
        # self.BTN.setFixedSize(5, 5)

        # OBJECTS ---------------------------
        # self.BTN.setFont(...)

        # self.BTN.setIcon(...)
        # self.BTN.setIconSize(...)

        # DONT UNDERSTAND -------------------
        # self.BTN.setAutoRepeat(True)
        # self.BTN.setAutoRepeatDelay(2)
        # self.BTN.setAutoRepeatInterval(2)

        # PROPERTIES ------------------------
        # print(self.BTN.isEnabled())
        # print(self.BTN.isCheckable())
        # print(self.BTN.isChecked())
        # print(self.BTN.isDown())
        # print(self.BTN.isFlat())
        # print(self.BTN.isHidden())
        # print(self.BTN.isVisible())
        # print(self.BTN.isDefault())

    def BTNS_PTE_create(self) -> None:
        # TODO: ADD BTNS_BLOCK!!! and apply here!!! used to explore PTE!!!
        # self.BTN_PTE = QPushButton("BTN")
        #
        # # SETTINGS -------------------------
        # self.BTN.setText("BTN_mod")
        # self.BTN.setToolTip("ToolTip")
        #
        # self.BTN.setCheckable(True)
        pass

    def CB_create(self) -> None:
        self.CB = QCheckBox("CB_text")

        # SETTINGS -------------------------
        # self.CB.setText("CB_text")
        self.CB.setText("CB_text")
        self.CB.setTristate()
        # ObjectInfo(self.CB).print()
        """
==========================================================================================
----------OBJECTINFO.PRINT--------------------------------------------------------------------------
str(SOURCE)=<PyQt5.QtWidgets.QCheckBox object at 0x000001A37592DEA0>
repr(SOURCE)=<PyQt5.QtWidgets.QCheckBox object at 0x000001A37592DEA0>
type(SOURCE)=<class 'PyQt5.QtWidgets.QCheckBox'>
mro(SOURCE)=['QCheckBox', 'QAbstractButton', 'QWidget', 'QObject', 'wrapper', 'QPaintDevice', 'simplewrapper', 'object']
----------SETTINGS----------------------------------------------------------------------------------
self.NAMES__USE_ONLY_PARTS=[]
self.NAMES__SKIP_FULL=[]
self.NAMES__SKIP_PARTS=['init', 'new', 'create', 'enter', 'install', 'set', 'clone', 'copy', 'move', 'next', 'clear', 'reduce', 'close', 'del', 'exit', 'kill', 'exec', 'exec_', 'pyqtConfigure', 'checkout', 'detach', 'run', 'start', 'wait', 'join', 'terminate', 'quit', 'disconnect', 'pop', 'popleft', 'append', 'appendleft', 'extend', 'extendleft', 'add', 'insert', 'reverse', 'rotate', 'sort']
self.HIDE_BUILD_IN=None
self.LOG_ITER=None
self.MAX_LINE_LEN=100
self.MAX_ITER_ITEMS=5
----------log_iter(wait last touched)---------------------------------------------------------------
----------SKIPPED_FULLNAMES-------------------------------------------------------------------------
----------SKIPPED_PARTNAMES-------------------------------------------------------------------------
1:	__delattr__
2:	__init__
3:	__init_subclass__
4:	__new__
5:	__reduce__
6:	__reduce_ex__
7:	__setattr__
8:	addAction
9:	addActions
10:	clearFocus
11:	clearMask
12:	close
13:	closeEvent
14:	create
15:	createWindowContainer
16:	deleteLater
17:	disconnect
18:	disconnectNotify
19:	enterEvent
20:	initPainter
21:	initStyleOption
22:	insertAction
23:	insertActions
24:	installEventFilter
25:	killTimer
26:	move
27:	moveEvent
28:	moveToThread
29:	nextCheckState
30:	nextInFocusChain
31:	pyqtConfigure
32:	removeAction
33:	removeEventFilter
34:	setAcceptDrops
35:	setAccessibleDescription
36:	setAccessibleName
37:	setAttribute
38:	setAutoExclusive
39:	setAutoFillBackground
40:	setAutoRepeat
41:	setAutoRepeatDelay
42:	setAutoRepeatInterval
43:	setBackgroundRole
44:	setBaseSize
45:	setCheckState
46:	setCheckable
47:	setChecked
48:	setContentsMargins
49:	setContextMenuPolicy
50:	setCursor
51:	setDisabled
52:	setDown
53:	setEnabled
54:	setFixedHeight
55:	setFixedSize
56:	setFixedWidth
57:	setFocus
58:	setFocusPolicy
59:	setFocusProxy
60:	setFont
61:	setForegroundRole
62:	setGeometry
63:	setGraphicsEffect
64:	setHidden
65:	setIcon
66:	setIconSize
67:	setInputMethodHints
68:	setLayout
69:	setLayoutDirection
70:	setLocale
71:	setMask
72:	setMaximumHeight
73:	setMaximumSize
74:	setMaximumWidth
75:	setMinimumHeight
76:	setMinimumSize
77:	setMinimumWidth
78:	setMouseTracking
79:	setObjectName
80:	setPalette
81:	setParent
82:	setProperty
83:	setShortcut
84:	setShortcutAutoRepeat
85:	setShortcutEnabled
86:	setSizeIncrement
87:	setSizePolicy
88:	setStatusTip
89:	setStyle
90:	setStyleSheet
91:	setTabOrder
92:	setTabletTracking
93:	setText
94:	setToolTip
95:	setToolTipDuration
96:	setTristate
97:	setUpdatesEnabled
98:	setVisible
99:	setWhatsThis
100:	setWindowFilePath
101:	setWindowFlag
102:	setWindowFlags
103:	setWindowIcon
104:	setWindowIconText
105:	setWindowModality
106:	setWindowModified
107:	setWindowOpacity
108:	setWindowRole
109:	setWindowState
110:	setWindowTitle
111:	startTimer
112:	unsetCursor
113:	unsetLayoutDirection
114:	unsetLocale
----------PROPERTIES__ELEMENTARY_SINGLE-------------------------------------------------------------
DrawChildren        	RenderFlag  :2
DrawWindowBackground	RenderFlag  :1
IgnoreMask          	RenderFlag  :4
PdmDepth            	PaintDeviceMetric:6
PdmDevicePixelRatio 	PaintDeviceMetric:11
PdmDevicePixelRatioScaled	PaintDeviceMetric:12
PdmDpiX             	PaintDeviceMetric:7
PdmDpiY             	PaintDeviceMetric:8
PdmHeight           	PaintDeviceMetric:2
PdmHeightMM         	PaintDeviceMetric:4
PdmNumColors        	PaintDeviceMetric:5
PdmPhysicalDpiX     	PaintDeviceMetric:9
PdmPhysicalDpiY     	PaintDeviceMetric:10
PdmWidth            	PaintDeviceMetric:1
PdmWidthMM          	PaintDeviceMetric:3
__doc__             	str         :QCheckBox(parent: Optional[QWidget] = None)
QCheckBox(text: ...
__module__          	str         :PyQt5.QtWidgets
__weakref__         	NoneType    :None
----------PROPERTIES__ELEMENTARY_COLLECTION---------------------------------------------------------
__dict__            	dict        :{}
----------PROPERTIES__OBJECTS-----------------------------------------------------------------------
staticMetaObject    	QMetaObject :<PyQt5.QtCore.QMetaObject object at 0x000001A3759622D0>
----------PROPERTIES__EXX---------------------------------------------------------------------------
----------METHODS__ELEMENTARY_SINGLE----------------------------------------------------------------
PaintDeviceMetric   	PaintDeviceMetric:0
RenderFlag          	RenderFlag  :0
__getstate__        	NoneType    :None
__hash__            	int         :112597741034
__repr__            	str         :<PyQt5.QtWidgets.QCheckBox object at 0x000001A37592DEA0>
__sizeof__          	int         :120
__str__             	str         :<PyQt5.QtWidgets.QCheckBox object at 0x000001A37592DEA0>
acceptDrops         	bool        :False
accessibleDescription	str         :
accessibleName      	str         :
activateWindow      	NoneType    :None
adjustSize          	NoneType    :None
animateClick        	NoneType    :None
autoExclusive       	bool        :False
autoFillBackground  	bool        :False
autoRepeat          	bool        :False
autoRepeatDelay     	int         :300
autoRepeatInterval  	int         :100
backgroundRole      	ColorRole   :1
checkState          	CheckState  :0
checkStateSet       	NoneType    :None
click               	NoneType    :None
colorCount          	int         :256
contextMenuPolicy   	ContextMenuPolicy:1
depth               	int         :32
destroy             	NoneType    :None
devType             	int         :1
devicePixelRatio    	int         :1
devicePixelRatioF   	float       :1.0
devicePixelRatioFScale	float       :65536.0
dumpObjectInfo      	NoneType    :None
dumpObjectTree      	NoneType    :None
effectiveWinId      	NoneType    :None
ensurePolished      	NoneType    :None
focusNextChild      	bool        :False
focusPolicy         	FocusPolicy :11
focusPreviousChild  	bool        :False
focusProxy          	NoneType    :None
foregroundRole      	ColorRole   :0
grabKeyboard        	NoneType    :None
grabMouse           	NoneType    :None
graphicsEffect      	NoneType    :None
graphicsProxyWidget 	NoneType    :None
group               	NoneType    :None
hasFocus            	bool        :False
hasHeightForWidth   	bool        :False
hasMouseTracking    	bool        :True
hasTabletTracking   	bool        :False
height              	int         :17
heightMM            	int         :3
hide                	NoneType    :None
isActiveWindow      	bool        :False
isCheckable         	bool        :True
isChecked           	bool        :True
isDown              	bool        :False
isEnabled           	bool        :True
isFullScreen        	bool        :False
isHidden            	bool        :True
isLeftToRight       	bool        :True
isMaximized         	bool        :False
isMinimized         	bool        :False
isModal             	bool        :False
isRightToLeft       	bool        :False
isTristate          	bool        :False
isVisible           	bool        :False
isWidgetType        	bool        :True
isWindow            	bool        :True
isWindowModified    	bool        :False
isWindowType        	bool        :False
layout              	NoneType    :None
layoutDirection     	LayoutDirection:0
logicalDpiX         	int         :96
logicalDpiY         	int         :96
lower               	NoneType    :None
maximumHeight       	int         :16777215
maximumWidth        	int         :16777215
minimumHeight       	int         :0
minimumWidth        	int         :0
nativeParentWidget  	NoneType    :None
objectName          	str         :
paintEngine         	NoneType    :None
paintingActive      	bool        :False
parent              	NoneType    :None
parentWidget        	NoneType    :None
physicalDpiX        	int         :109
physicalDpiY        	int         :109
raise_              	NoneType    :None
releaseKeyboard     	NoneType    :None
releaseMouse        	NoneType    :None
repaint             	NoneType    :None
sender              	NoneType    :None
senderSignalIndex   	int         :-1
sharedPainter       	NoneType    :None
show                	NoneType    :None
showFullScreen      	NoneType    :None
showMaximized       	NoneType    :None
showMinimized       	NoneType    :None
showNormal          	NoneType    :None
signalsBlocked      	bool        :False
statusTip           	str         :
styleSheet          	str         :
text                	str         :CB_text
toggle              	NoneType    :None
toolTip             	str         :
toolTipDuration     	int         :-1
underMouse          	bool        :False
update              	NoneType    :None
updateGeometry      	NoneType    :None
updateMicroFocus    	NoneType    :None
updatesEnabled      	bool        :True
whatsThis           	str         :
width               	int         :2560
widthMM             	int         :597
windowFilePath      	str         :
windowIconText      	str         :
windowModality      	WindowModality:0
windowOpacity       	float       :1.0
windowRole          	str         :
windowTitle         	str         :
windowType          	WindowType  :1
x                   	int         :2559
y                   	int         :-7
----------METHODS__ELEMENTARY_COLLECTION------------------------------------------------------------
__dir__             	list        :['__module__', '__doc__', 'actionEvent', 'changeEvent', 'che...
                    	str         :	__module__
                    	str         :	__doc__
                    	str         :	actionEvent
                    	str         :	changeEvent
                    	str         :	checkState
                    	            :	...
actions             	list        :[]
children            	list        :[]
dynamicPropertyNames	list        :[]
getContentsMargins  	tuple       :(0, 0, 0, 0)
----------METHODS__OBJECTS--------------------------------------------------------------------------
RenderFlags         	RenderFlags :<PyQt5.QtWidgets.QWidget.RenderFlags object at 0x000001A375960D60>
__class__           	QCheckBox   :<PyQt5.QtWidgets.QCheckBox object at 0x000001A37592DFC0>
__subclasshook__    	NotImplementedType:NotImplemented
baseSize            	QSize       :PyQt5.QtCore.QSize()
childrenRect        	QRect       :PyQt5.QtCore.QRect()
childrenRegion      	QRegion     :<PyQt5.QtGui.QRegion object at 0x000001A375961460>
contentsMargins     	QMargins    :<PyQt5.QtCore.QMargins object at 0x000001A375961540>
contentsRect        	QRect       :PyQt5.QtCore.QRect(0, 0, 62, 17)
cursor              	QCursor     :<PyQt5.QtGui.QCursor object at 0x000001A375961620>
focusWidget         	QCheckBox   :<PyQt5.QtWidgets.QCheckBox object at 0x000001A37592DEA0>
font                	QFont       :<PyQt5.QtGui.QFont object at 0x000001A3759618C0>
fontInfo            	QFontInfo   :<PyQt5.QtGui.QFontInfo object at 0x000001A375961930>
fontMetrics         	QFontMetrics:<PyQt5.QtGui.QFontMetrics object at 0x000001A3759619A0>
frameGeometry       	QRect       :PyQt5.QtCore.QRect(0, 0, 61, 16)
frameSize           	QSize       :PyQt5.QtCore.QSize(61, 16)
geometry            	QRect       :PyQt5.QtCore.QRect(0, 0, 62, 17)
grab                	QPixmap     :<PyQt5.QtGui.QPixmap object at 0x000001A375961B60>
icon                	QIcon       :<PyQt5.QtGui.QIcon object at 0x000001A37592E050>
iconSize            	QSize       :PyQt5.QtCore.QSize(16, 16)
inputMethodHints    	InputMethodHints:<PyQt5.QtCore.Qt.InputMethodHints object at 0x000001A375...
keyboardGrabber     	QCheckBox   :<PyQt5.QtWidgets.QCheckBox object at 0x000001A37592DEA0>
locale              	QLocale     :<PyQt5.QtCore.QLocale object at 0x000001A375961FC0>
mask                	QRegion     :<PyQt5.QtGui.QRegion object at 0x000001A3759621F0>
maximumSize         	QSize       :PyQt5.QtCore.QSize(16777215, 16777215)
metaObject          	QMetaObject :<PyQt5.QtCore.QMetaObject object at 0x000001A3759622D0>
minimumSize         	QSize       :PyQt5.QtCore.QSize()
minimumSizeHint     	QSize       :PyQt5.QtCore.QSize(62, 17)
mouseGrabber        	QCheckBox   :<PyQt5.QtWidgets.QCheckBox object at 0x000001A37592DEA0>
normalGeometry      	QRect       :PyQt5.QtCore.QRect(0, 0, 62, 17)
palette             	QPalette    :<PyQt5.QtGui.QPalette object at 0x000001A375962490>
pos                 	QPoint      :PyQt5.QtCore.QPoint()
previousInFocusChain	QCheckBox   :<PyQt5.QtWidgets.QCheckBox object at 0x000001A37592DEA0>
rect                	QRect       :PyQt5.QtCore.QRect(0, 0, 62, 17)
saveGeometry        	QByteArray  :b'\x01\xd9\xd0\xcb\x00\x03\x00\x00\x00\x00\x00\x00\x00\x00...
screen              	QScreen     :<PyQt5.QtGui.QScreen object at 0x000001A37592E0E0>
shortcut            	QKeySequence:<PyQt5.QtGui.QKeySequence object at 0x000001A3759627A0>
size                	QSize       :PyQt5.QtCore.QSize(2560, 1377)
sizeHint            	QSize       :PyQt5.QtCore.QSize(62, 17)
sizeIncrement       	QSize       :PyQt5.QtCore.QSize()
sizePolicy          	QSizePolicy :<PyQt5.QtWidgets.QSizePolicy object at 0x000001A3759629D0>
style               	QCommonStyle:<PyQt5.QtWidgets.QCommonStyle object at 0x000001A37592E170>
thread              	QThread     :<PyQt5.QtCore.QThread object at 0x000001A37592E200>
visibleRegion       	QRegion     :<PyQt5.QtGui.QRegion object at 0x000001A375962B90>
winId               	voidptr     :<sip.voidptr object at 0x000001A3759FE9D0>
window              	QCheckBox   :<PyQt5.QtWidgets.QCheckBox object at 0x000001A37592DEA0>
windowFlags         	WindowFlags :<PyQt5.QtCore.Qt.WindowFlags object at 0x000001A375962C00>
windowHandle        	QWindow     :<PyQt5.QtGui.QWindow object at 0x000001A37592E290>
windowIcon          	QIcon       :<PyQt5.QtGui.QIcon object at 0x000001A37592E320>
windowState         	WindowStates:<PyQt5.QtCore.Qt.WindowStates object at 0x000001A375962C70>
----------METHODS__EXX------------------------------------------------------------------------------
__eq__              	TypeError   :TypeError('expected 1 argument, got 0')
__format__          	TypeError   :TypeError('QCheckBox.__format__() takes exactly one argument...
__ge__              	TypeError   :TypeError('expected 1 argument, got 0')
__getattr__         	TypeError   :TypeError('__getattr__(self, name: Optional[str]): not enoug...
__getattribute__    	TypeError   :TypeError('expected 1 argument, got 0')
__gt__              	TypeError   :TypeError('expected 1 argument, got 0')
__le__              	TypeError   :TypeError('expected 1 argument, got 0')
__lt__              	TypeError   :TypeError('expected 1 argument, got 0')
__ne__              	TypeError   :TypeError('expected 1 argument, got 0')
actionEvent         	TypeError   :TypeError('actionEvent(self, a0: Optional[QActionEvent]): no...
blockSignals        	TypeError   :TypeError('blockSignals(self, b: bool): not enough arguments')
changeEvent         	TypeError   :TypeError('changeEvent(self, e: Optional[QEvent]): not enoug...
childAt             	TypeError   :TypeError('arguments did not match any overloaded call:\n  c...
childEvent          	TypeError   :TypeError('childEvent(self, a0: Optional[QChildEvent]): not ...
clicked             	TypeError   :TypeError('native Qt signal is not callable')
connectNotify       	TypeError   :TypeError('connectNotify(self, signal: QMetaMethod): not eno...
contextMenuEvent    	TypeError   :TypeError('contextMenuEvent(self, a0: Optional[QContextMenuE...
customContextMenuRequested	TypeError   :TypeError('native Qt signal is not callable')
customEvent         	TypeError   :TypeError('customEvent(self, a0: Optional[QEvent]): not enou...
destroyed           	TypeError   :TypeError('native Qt signal is not callable')
dragEnterEvent      	TypeError   :TypeError('dragEnterEvent(self, a0: Optional[QDragEnterEvent...
dragLeaveEvent      	TypeError   :TypeError('dragLeaveEvent(self, a0: Optional[QDragLeaveEvent...
dragMoveEvent       	TypeError   :TypeError('dragMoveEvent(self, a0: Optional[QDragMoveEvent])...
dropEvent           	TypeError   :TypeError('dropEvent(self, a0: Optional[QDropEvent]): not en...
event               	TypeError   :TypeError('event(self, e: Optional[QEvent]): not enough argu...
eventFilter         	TypeError   :TypeError('eventFilter(self, a0: Optional[QObject], a1: Opti...
find                	TypeError   :TypeError('find(a0: PyQt5.sip.voidptr): not enough arguments')
findChild           	TypeError   :TypeError("arguments did not match any overloaded call:\n  f...
findChildren        	TypeError   :TypeError("arguments did not match any overloaded call:\n  f...
focusInEvent        	TypeError   :TypeError('focusInEvent(self, e: Optional[QFocusEvent]): not...
focusNextPrevChild  	TypeError   :TypeError('focusNextPrevChild(self, next: bool): not enough ...
focusOutEvent       	TypeError   :TypeError('focusOutEvent(self, e: Optional[QFocusEvent]): no...
grabGesture         	TypeError   :TypeError('grabGesture(self, type: Qt.GestureType, flags: Un...
grabShortcut        	TypeError   :TypeError('grabShortcut(self, key: Union[QKeySequence, QKeyS...
heightForWidth      	TypeError   :TypeError('heightForWidth(self, a0: int): not enough arguments')
hideEvent           	TypeError   :TypeError('hideEvent(self, a0: Optional[QHideEvent]): not en...
hitButton           	TypeError   :TypeError('hitButton(self, pos: QPoint): not enough arguments')
inherits            	TypeError   :TypeError('inherits(self, classname: Optional[str]): not eno...
inputMethodEvent    	TypeError   :TypeError('inputMethodEvent(self, a0: Optional[QInputMethodE...
inputMethodQuery    	TypeError   :TypeError('inputMethodQuery(self, a0: Qt.InputMethodQuery): ...
isAncestorOf        	TypeError   :TypeError('isAncestorOf(self, child: Optional[QWidget]): not...
isEnabledTo         	TypeError   :TypeError('isEnabledTo(self, a0: Optional[QWidget]): not eno...
isSignalConnected   	TypeError   :TypeError('isSignalConnected(self, signal: QMetaMethod): not...
isVisibleTo         	TypeError   :TypeError('isVisibleTo(self, a0: Optional[QWidget]): not eno...
keyPressEvent       	TypeError   :TypeError('keyPressEvent(self, e: Optional[QKeyEvent]): not ...
keyReleaseEvent     	TypeError   :TypeError('keyReleaseEvent(self, e: Optional[QKeyEvent]): no...
leaveEvent          	TypeError   :TypeError('leaveEvent(self, a0: Optional[QEvent]): not enoug...
mapFrom             	TypeError   :TypeError('mapFrom(self, a0: Optional[QWidget], a1: QPoint):...
mapFromGlobal       	TypeError   :TypeError('mapFromGlobal(self, a0: QPoint): not enough arguments')
mapFromParent       	TypeError   :TypeError('mapFromParent(self, a0: QPoint): not enough arguments')
mapTo               	TypeError   :TypeError('mapTo(self, a0: Optional[QWidget], a1: QPoint): n...
mapToGlobal         	TypeError   :TypeError('mapToGlobal(self, a0: QPoint): not enough arguments')
mapToParent         	TypeError   :TypeError('mapToParent(self, a0: QPoint): not enough arguments')
metric              	TypeError   :TypeError('metric(self, a0: QPaintDevice.PaintDeviceMetric):...
mouseDoubleClickEvent	TypeError   :TypeError('mouseDoubleClickEvent(self, a0: Optional[QMouseE...
mouseMoveEvent      	TypeError   :TypeError('mouseMoveEvent(self, a0: Optional[QMouseEvent]): ...
mousePressEvent     	TypeError   :TypeError('mousePressEvent(self, e: Optional[QMouseEvent]): ...
mouseReleaseEvent   	TypeError   :TypeError('mouseReleaseEvent(self, e: Optional[QMouseEvent])...
nativeEvent         	TypeError   :TypeError('nativeEvent(self, eventType: Union[QByteArray, by...
objectNameChanged   	TypeError   :TypeError('native Qt signal is not callable')
overrideWindowFlags 	TypeError   :TypeError('overrideWindowFlags(self, type: Union[Qt.WindowFl...
overrideWindowState 	TypeError   :TypeError('overrideWindowState(self, state: Union[Qt.WindowS...
paintEvent          	TypeError   :TypeError('paintEvent(self, a0: Optional[QPaintEvent]): not ...
pressed             	TypeError   :TypeError('native Qt signal is not callable')
property            	TypeError   :TypeError('property(self, name: Optional[str]): not enough a...
receivers           	TypeError   :TypeError('receivers(self, signal: PYQT_SIGNAL): not enough ...
releaseShortcut     	TypeError   :TypeError('releaseShortcut(self, id: int): not enough arguments')
released            	TypeError   :TypeError('native Qt signal is not callable')
render              	TypeError   :TypeError('arguments did not match any overloaded call:\n  r...
resize              	TypeError   :TypeError('arguments did not match any overloaded call:\n  r...
resizeEvent         	TypeError   :TypeError('resizeEvent(self, a0: Optional[QResizeEvent]): no...
restoreGeometry     	TypeError   :TypeError('restoreGeometry(self, geometry: Union[QByteArray,...
scroll              	TypeError   :TypeError('arguments did not match any overloaded call:\n  s...
showEvent           	TypeError   :TypeError('showEvent(self, a0: Optional[QShowEvent]): not en...
stackUnder          	TypeError   :TypeError('stackUnder(self, a0: Optional[QWidget]): not enou...
stateChanged        	TypeError   :TypeError('native Qt signal is not callable')
tabletEvent         	TypeError   :TypeError('tabletEvent(self, a0: Optional[QTabletEvent]): no...
testAttribute       	TypeError   :TypeError('testAttribute(self, attribute: Qt.WidgetAttribute...
timerEvent          	TypeError   :TypeError('timerEvent(self, e: Optional[QTimerEvent]): not e...
toggled             	TypeError   :TypeError('native Qt signal is not callable')
tr                  	TypeError   :TypeError('tr(self, sourceText: Optional[str], disambiguatio...
ungrabGesture       	TypeError   :TypeError('ungrabGesture(self, type: Qt.GestureType): not en...
wheelEvent          	TypeError   :TypeError('wheelEvent(self, a0: Optional[QWheelEvent]): not ...
windowIconChanged   	TypeError   :TypeError('native Qt signal is not callable')
windowIconTextChanged	TypeError   :TypeError('native Qt signal is not callable')
windowTitleChanged  	TypeError   :TypeError('native Qt signal is not callable')
==========================================================================================
        """

    def TV_create(self) -> None:
        # PREPARE ------------------------
        if self.DATA is None:
            self.DATA = Data_([Row_(f"row{index}") for index in range(5)], [Dev_(f"dev{index}") for index in range(4)])

        self.TM = TableModelTemplate(self.DATA)

        # WORK ---------------------------
        self.TV = QTableView()
        self.TV.setModel(self.TM)

        # STYLE -----
        # self.TV.setShowGrid(True)
        # self.TV.setFont(QFont("Calibri (Body)", 12))  # сразу на все!!! и на заголоски и на ячейки
        # self.TV.setStyleSheet("gridline-color: rgb(255, 0, 0)")

        # self.TV.setSortingEnabled(True)     # enable sorting

        # HEADER ---------
        self.TV.setHorizontalHeader(HeaderViewCB(self.DATA))   # you can add some additional HV object!

        # hh = self.TV.horizontalHeader()
        # hh.setStretchLastSection(True)
        # hh.setSectionsClickable(False)
        # hh.setSectionsMovable(False)
        # hh.setVisible(False)
        # hh.swapSections(1,2)

        # GEOMETRY  ----------
        # self.TV.setMinimumSize(400, 300)
        # self.TV.resize(400, 300)
        # self.TV.setColumnWidth(0, 100)
        self.TV.resizeColumnsToContents()   # set column width to fit contents - NEED AFTER SetHEADER!!!

    def PTE_create(self) -> None:
        self.PTE = QPlainTextEdit()

        # METHODS ORIGINAL ---------------------------------
        # self.PTE.setEnabled(True)
        # self.PTE.setUndoRedoEnabled(True)
        # self.PTE.setReadOnly(True)
        # self.PTE.setMaximumBlockCount(15)

        # self.PTE.clear()
        self.PTE.setPlainText("setPlainText")
        self.PTE.appendPlainText("appendPlainText")
        self.PTE.appendPlainText("result=None")
        self.PTE.appendPlainText("result=True")
        self.PTE.appendPlainText("result=False")
        # self.PTE.appendHtml("")
        # self.PTE.anchorAt(#)
        # self.PTE.setSizeAdjustPolicy(#)

        # METHODS COMMON -----------------------------------
        self.PTE.setFont(QFont("Calibri (Body)", 7))

        # ObjectInfo(self.PTE).print()

        # BODY
        # body: str = self.PTE.toPlainText()

    def HL_create(self) -> None:
        if self.HL_STYLES and self.PTE:
            self.HL = Highlighter(document=self.PTE.document(), styles=self.HL_STYLES)

    # SLOTS ===========================================================================================================
    def slots_connect(self) -> None:
        if self.BTN:
            self.BTN.clicked.connect(self._wgt_main__center)
            if self.BTN.isCheckable():
                self.BTN.toggled.connect(self.BTN__toggled)
            else:
                self.BTN.clicked.connect(self.BTN__toggled)

        if self.CB:
            self.CB.stateChanged.connect(self.CB__changed)

        if self.TV:
            self.TV.selectionModel().selectionChanged.connect(self.TV_selectionChanged)
            # self.TV.horizontalHeader().sectionClicked.connect(self.TV_hh_sectionClicked)

    def BTN__toggled(self, state: Optional[bool] = None) -> None:
        print(f"BTN__toggled {state=}")

    def CB__changed(self, state: Optional[int] = None) -> None:
        """
        :param state:
            0 - unchecked
            1 - halfCHecked (only if isTristate)
            2 - checked (even if not isTristate)
        """
        print(f"CB__changed {state=}")

    def TV_selectionChanged(self, first: QItemSelection, last: QItemSelection) -> None:
        # print("selectionChanged")
        # print(f"{first=}")  # first=<PyQt5.QtCore.QItemSelection object at 0x000001C79A107460>
        # ObjectInfo(first.indexes()[0]).print(_log_iter=True, skip_fullnames=["takeFirst", "takeLast"])

        # print(f"{first=}")

        if not first:
            print(f"selected first NotSelectable Index {first=}")
            return

        try:
            index: QModelIndex = first.indexes()[0]
        except:
            return

        row = index.row()
        col = index.column()

        self.PTE.setPlainText(f"{row=}/{col=}")

    # EVENTS ==========================================================================================================
    pass    # events list see in source code!
    pass    # events list see in source code!
    pass    # events list see in source code!
    pass    # events list see in source code!
    pass    # events list see in source code!

    # def mouseMoveEvent(self, a0: typing.Optional[QtGui.QMouseEvent]) -> None: ...

    def moveEvent(self,  a0: Optional[QMoveEvent] = None, QMoveEvent: Any = None) -> None:
        # print(self.geometry().x(), self.geometry().y())
        pass

    def resizeEvent(self, a0: Optional[QResizeEvent] = None, ResizeEvent: Any = None) -> None:
        # print(self.size())
        pass

    # mouse POINTER -------------------------------------------------
    def enterEvent(self, a0: Optional[QEvent] = None) -> None:
        """mouse get aria over the wgt
        """
        # print("mouse enterEvent")
        pass

    def leaveEvent(self, a0: Optional[QEvent] = None) -> None:
        """mouse leave aria over the wgt
        """
        # print("mouse leaveEvent")
        pass

    # mouse CLICK -------------------------------------------------
    def mousePressEvent(self, a0: Optional[QMouseEvent] = None) -> None:
        """will not apply when click on wgt btns!"""
        # print("mouse mousePressEvent")
        pass

    def mouseDoubleClickEvent(self, a0: Optional[QMouseEvent] = None) -> None:
        """will not apply when click on wgt btns!
        DIFFERENCE between DoubleClick and PressEvent
            if detected DoubleClick it will generate DoubleClickEvent else PressEvent
                mouse mousePressEvent
                mouse mouseReleaseEvent
                mouse mouseDoubleClickEvent
                mouse mouseReleaseEvent
        """
        # print("mouse mouseDoubleClickEvent")
        pass

    def mouseReleaseEvent(self, a0: Optional[QMouseEvent] = None) -> None:
        """
        work always! both for One/Double click!
            mouse mousePressEvent
            mouse mouseReleaseEvent
            mouse mouseDoubleClickEvent
            mouse mouseReleaseEvent
        """
        # print("mouse mouseReleaseEvent")
        pass

    # NOT WORKING ------------------------------------------
    # def focusOutEvent(self, a0: Optional[QEvent]) -> None:
    #     """mouse leave aria over the wgt
    #     """
    #     # print("focusOutEvent")
    #     pass
    #
    # def focusInEvent(self, a0: Optional[QEvent]) -> None:
    #     """mouse leave aria over the wgt
    #     """
    #     # print("focusInEvent")
    #     pass


# =====================================================================================================================
