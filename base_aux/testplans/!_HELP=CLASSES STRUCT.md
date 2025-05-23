COMMON INFO
===========

DUT - exact testing device (PSU)
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

TP_ITEMS - collection of all existed TP
--------
	n1: TP_ITEM
	n2: TP_ITEM


TP_ITEM - full set for one exact TP (final instances)
-------
	NAME
	DESCRIPTION
	SN      # mean Sn of stand (SN intended get from UART fo main/root device)

	DEV_LINES: TableKit     # all devices need in TP
	TCSc_LINE: Tableline    # TC classes in TP (iterable)


TC
--
	TP_ITEM: TP_ITEM     - access to all none indexed instances
	TP_ITEM.DEV_LINES
	TP_ITEM.TCSc_LINE

	DEV_COLUMN: TableColumn  # access to exact device by name from lists by same Index
	TCSi_LINE: Tableline   # access to all instances of self-class
