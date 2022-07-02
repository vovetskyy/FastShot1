echo off
rem 
rem 1st parameter -- number of measurement loops (default value see in main.py)


set CUR_PATH=%cd%
set PC_NAME=%COMPUTERNAME%

set NORM_OUT=%CUR_PATH%\RawOutput\%PC_NAME%_Test1.txt

rem %CUR_PATH%\venv\Scripts\python.exe %CUR_PATH%\main.py 4 > %CUR_PATH%\RawOutput\Test1.txt 2>error.log
%CUR_PATH%\venv\Scripts\python.exe %CUR_PATH%\main.py 4 >%NORM_OUT% 2>error.log