rem ====================================
rem VERSION = (0, 0, 1)  # add rule 1
rem VERSION = (0, 0, 2)  # move tests into base_aux directory!
rem VERSION = (0, 0, 3)  # add COV into HTML

rem ====================================
REM RULES:
REM 1. in all files (all docstrings) reuse single slash '\*' into double '\\*'!
rem otherwise it will get WARNING in pytest

rem ====================================
echo off
cls

pytest ^
    --cov-config=.coveragerc^
    --cov=base_aux^
    --cov-report html

pause
