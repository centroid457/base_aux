COMMON INFO
===========

DUT (Device Under Test) - exact testing device (PSU)
---

INDEX
-----
    COUNT=12 - how many devices could testing in stand (12 psu in QTC)
    for device and testcase
    we need generate some exact count of TC instances
    and in all TcInst apply same Index for devices

DEV_COLUMN
----------
    if
        DEV_LINES:
            ATC_: TableLine = TableLine(1)
            PTB_: TableLine = TableLine(1,2,3)
    then
        DEV_COLUMN.ATC_ = DEV_LINES.ATC_[self.INDEX] = 1
        DEV_COLUMN.PTB_ = DEV_LINES.PTB_[self.INDEX] = [1,2,3][self.INDEX]


EXACT classes
=============

TP_MANAGER
----------
    STANDS
    STAND

    tc_active


STANDS - collection of all existed TP/STANDS
--------
	n1: STAND
	n2: STAND


STAND - full set for one exact TP (final instances)
-------
    NAME
    DESCRIPTION
    SN      # mean Sn of stand (SN intended get from UART fo main/root device)
    
    DEV_LINES: TableKit     # all devices need in TP
    TCSc_LINE: Tableline    # TC classes in TP (iterable)
    
    ---INFO---
    stand__get_info__short
    stand__get_info__full
    stand__get_results
    stand__save_results
    
    RESULTS ???
    

TC
--
	STAND: STAND     - access to all none indexed instances
	STAND.DEV_LINES
	STAND.TCSc_LINE

	DEV_COLUMN: TableColumn  # access to exact device by name from lists by same Index
	TCSi_LINE: Tableline   # access to all instances of self-class


DEVICE
--------
    NAME: str
    DESCRIPTION: str
    INDEX: int

    DEV_FOUND: bool | None

    SN: str
    FW: str
    MODEL: str

    dev__load_info
    dev__get_info



RESULTS -???
------------  
    - Gen from STAND as final instance
    - make on TableLines ??? to use Column
    - apply save results in result-Object
    - add str
