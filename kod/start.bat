@echo off
cd /d "%~dp0"
echo ============================================================
echo   USEME CORE ENGINE
echo ============================================================
set "PY_CMD=python"
if exist "%~dp0.venv\Scripts\python.exe" set "PY_CMD=%~dp0.venv\Scripts\python.exe"
"%PY_CMD%" -u engine.py %*
pause
