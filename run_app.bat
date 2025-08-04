@echo off
echo Starting Banking Management System...
echo.

REM Activate virtual environment and run the app
call banking_env\Scripts\activate.bat
python main.py

echo.
echo Application closed.
pause 