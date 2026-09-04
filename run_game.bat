@echo off
title Neon Nexus
cd /d "%~dp0"
call .venv\Scripts\activate.bat
python neon_nexus\main.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Game exited with error code %ERRORLEVEL%
    pause
)
