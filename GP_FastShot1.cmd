echo off
rem 
rem 1st parameter -- number of measurement loops (default value see in main.py)


set CUR_PATH=%cd%
echo %CUR_PATH%

%CUR_PATH%\venv\Scripts\python.exe %CUR_PATH%\main.py 4 > %CUR_PATH%\RawOutput\Test1.txt