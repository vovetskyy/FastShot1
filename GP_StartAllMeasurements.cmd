echo off
rem
rem 1st parameter -- number of measurement loops (default value -- %DEF_NUM_LOOPS%)
set NUM_LOOPS="%1"
set DEF_NUM_LOOPS=5
if %NUM_LOOPS%=="" set NUM_LOOPS=%DEF_NUM_LOOPS%

set CUR_PATH=%cd%
set PC_NAME=%COMPUTERNAME%
set INTEL_PG_PATH="c:\Program Files\Intel\Power Gadget 3.6"

set INTEL_PG_CSV_OUT="%CUR_PATH%\RawOutput\%PC_NAME%_IPG.csv"
set SCRIPT1_OUT="%CUR_PATH%\RawOutput\%PC_NAME%_Script1.txt"

echo on

rem %INTEL_PG_PATH%\PowerLog3.0.exe -file %INTEL_PG_CSV_OUT% -duration 2
%INTEL_PG_PATH%\PowerLog3.0.exe -file %INTEL_PG_CSV_OUT% -resolution 500 -cmd "GP_FastShot1.cmd %SCRIPT1_OUT% %NUM_LOOPS%"