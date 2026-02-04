@echo off
setlocal enabledelayedexpansion

:check_setup
if exist "src/.setup_done" (
    echo [PHASE 1] Setup already completed. Skipping to menu...
    goto :run_script
)

:setup
echo [PHASE 1] Verifying system requirements...
where curl.exe >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] curl.exe not found. This script requires Windows 10/11.
    pause
    exit /b 1
)

if exist "LICENSE" (
    type "LICENSE"
    echo.
) else (
    echo [ERROR] LICENSE file not found.
    exit /b 1
)

set /p choice="Do you accept the license terms? (y/n): "
if /i "%choice%" neq "y" exit /b 0

echo [PHASE 2] Checking Python environment...
python --version 2>nul | findstr /C:"3.14.2" >nul
if %errorlevel% neq 0 (
    echo [INFO] Python 3.14.2 not found. Downloading installer...
    curl.exe -o python_installer.exe https://www.python.org/ftp/python/3.14.2/python-3.14.2-amd64.exe
    echo [INFO] Installing Python... Please wait.
    start /wait python_installer.exe /quiet InstallAllUsers=1 PrependPath=1
    del python_installer.exe
)

echo [PHASE 3] Configuring Python dependencies...
pip install --quiet pipenv
if exist "Pipfile" (
    echo [INFO] Running pipenv install...
    pipenv install
)

echo [PHASE 4] Verifying integrity of files...
pipenv run python src/integrity.py
if %errorlevel% neq 0 (
    echo [CRITICAL] Integrity check failed.
    pause
    exit /b 1
)

echo. > src/.setup_done
echo [SUCCESS] Environment is ready.
timeout /t 2 >nul

:run_script
cls
:: Read version from src/version
set "ver_val=Unknown"
if exist "src\version" (
    set /p ver_val=<"src\version"
)

echo      _____          __  .__  .__          __  .__           ___________            .__          
echo     /  _  \________/  ^|_^|  ^| ^|__^| _______/  ^|_^|__^| ____     \__    ___/___   ____ ^|  ^|   ______ 
echo    /  /_\  \_  __ \   __\  ^| ^|  ^|/  ___/\   __\  ^|/  _ \      ^|    ^| /  _ \ /  _ \^|  ^|  /  ___/ 
echo   /    ^|    \  ^| \/^|  ^| ^|  ^|_^|  ^|\___ \  ^|  ^| ^|  ^|  ^<_^> )     ^|    ^|(  ^<_^> ^|  ^<_^> )  ^|__\___ \  
echo   \____^|__  /__^|   ^|__^| ^|____/__/____  ^> ^|__^| ^|__^|\____/      ^|____^| \____/ \____/^|____/____  ^> 
echo           \/                         \/                                                     \/  
echo                                     Author: Mu_rpy
echo                                     Version: %ver_val%
echo.
echo 1. Stock Footage Downloader
echo 2. SFX / Music Downloader
echo 3. Install Latest Updates
echo 4. Exit
echo.

set "menu="
set /p menu="Select an option (1-4): "

if "%menu%"=="1" (
    echo [RUN] Launching Stock Footage Downloader...
    pipenv run python src/artlistio-vid.py
    pause
    goto :run_script
)
if "%menu%"=="2" (
    echo [RUN] Launching SFX / Music Downloader...
    pipenv run python src/artlistio-sfx.py
    pause
    goto :run_script
)
if "%menu%"=="3" (
    echo [RUN] Checking for updates...
    pipenv run python src/updater.py
    pause
    goto :run_script
)
if "%menu%"=="4" exit /b 0

echo.
echo [ERROR] "%menu%" is an invalid selection.
timeout /t 2 >nul
goto :run_script