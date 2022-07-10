echo off

set CUR_PATH=%cd%
set PC_NAME=%COMPUTERNAME%
set INTEL_PG_PATH="c:\Program Files\Intel\Power Gadget 3.6"

set INTEL_PG_CSV_OUT=%CUR_PATH%\RawOutput\%PC_NAME%_IPG.csv

echo on

rem %INTEL_PG_PATH%\PowerLog3.0.exe -file %INTEL_PG_CSV_OUT% -duration 2
%INTEL_PG_PATH%\PowerLog3.0.exe -file %INTEL_PG_CSV_OUT% -resolution 500 -cmd GP_FastShot1.cmd