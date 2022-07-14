echo off
rem
rem -----------------------------------------------------------------
rem 1st parameter -- number of measurement loops (default value -- %DEF_NUM_LOOPS%)
set NUM_LOOPS="%1"
set DEF_NUM_LOOPS=5
if %NUM_LOOPS%=="" set NUM_LOOPS=%DEF_NUM_LOOPS%
rem -----------------------------------------------------------------

rem -----------------------------------------------------------------
rem setting of paths
set CUR_PATH=%cd%

rem UPDATE THE PATH IF NECESSARY
set INTEL_PG_PATH="c:\Program Files\Intel\Power Gadget 3.6"
rem -----------------------------------------------------------------


rem -----------------------------------------------------------------
rem definition of ouptut names (including PC-name and timestamp)

rem get timestamps
call GP_GetTimeStamp.cmd
rem now we have timestamp in the %FULL_TIMESTAMP%

set PC_NAME=%COMPUTERNAME%

set NAME_PREFIX=%PC_NAME%_%FULL_TIMESTAMP%


set INTEL_PG_CSV_OUT="%CUR_PATH%\RawOutput\%NAME_PREFIX%_IPG.csv"
set SCRIPT1_OUT="%CUR_PATH%\RawOutput\%NAME_PREFIX%_Script1.txt"

rem -----------------------------------------------------------------

rem -----------------------------------------------------------------
rem run measurements
echo on

rem %INTEL_PG_PATH%\PowerLog3.0.exe -file %INTEL_PG_CSV_OUT% -duration 2
%INTEL_PG_PATH%\PowerLog3.0.exe -file %INTEL_PG_CSV_OUT% -resolution 500 -cmd "GP_FastShot1.cmd %SCRIPT1_OUT% %NUM_LOOPS%"