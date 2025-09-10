@echo off
REM Setup and activate virtual environment for CCCS_106 projects

REM Navigate to the project folder
cd /d "%~dp0\cccs106-projects"

REM Check if the virtual environment folder exists
IF NOT EXIST "cccs106_env_bacsain" (
    echo Creating virtual environment...
    python -m venv cccs106_env_bacsain
)

REM Activate the virtual environment
call cccs106_env_bacsain\Scripts\activate.bat

REM Install requirements
IF EXIST "requirements.txt" (
    echo Installing packages from requirements.txt...
    pip install -r requirements.txt
) ELSE (
    echo requirements.txt not found. Skipping package installation.
)

REM Keep the terminal open
cmd
