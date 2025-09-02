@echo off
REM Activate the virtual environment for CCCS_106 projects

REM The project folder
cd /d "%~dp0\cccs106-projects"

REM Virtual environment activation
call cccs106_env_bacsain\Scripts\activate.bat

REM This is to keep the terminal open
cmd