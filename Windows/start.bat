@echo off
setlocal enabledelayedexpansion

:check_setup
if exist "src\data\.setup_done" (
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

if exist "src\data\LICENSE" (
    type "src\data\LICENSE"
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
    curl.exe -L -o python_installer.exe https://www.python.org/ftp/python/3.14.2/python-3.14.2-amd64.exe
    echo [INFO] Installing Python... Please wait.
    start /wait python_installer.exe /quiet InstallAllUsers=1 PrependPath=1
    del python_installer.exe
)
echo Verifying FFmpeg...
if not exist "src\ffmpeg.exe" (
    echo [INFO] FFmpeg not found. Downloading portable binary...
    curl.exe -L -o ffmpeg.zip https://github.com/GyanD/codexffmpeg/releases/download/7.1/ffmpeg-7.1-essentials_build.zip
    
    echo [INFO] Extracting...
    powershell -Command "Expand-Archive -Path ffmpeg.zip -DestinationPath temp_ffmpeg -Force"
    for /r "temp_ffmpeg" %%i in (ffmpeg.exe) do >nul 2>nul move /y "%%i" "src\"
    
    echo [INFO] Cleaning up...
    rd /s /q temp_ffmpeg
    del /f /q ffmpeg.zip
)

echo [PHASE 3] Configuring Python dependencies...
py -m pip install --quiet --upgrade pip
py -m pip install --quiet pipenv
if exist "Pipfile" (
    echo [INFO] Installing dependencies from Pipfile...
    pipenv install
) else (
    echo [INFO] Creating new environment and installing streamlink...
    pipenv install streamlink playwright
)
pipenv run python -m playwright install chromium

echo [PHASE 4] Verifying integrity of files...
pipenv run python src/integrity.py
if %errorlevel% neq 0 (
    echo [91m[CRITICAL] Integrity check failed.[0m
    set /p cont="Continue anyway? (Experimental Build) (y/n): "
    if /i "!cont!" neq "y" exit /b 1
)

echo. > src\data\.setup_done
echo [SUCCESS] Environment is ready.
timeout /t 2 >nul

:run_script
cls
set "ver_val=Unknown"
if exist "src\data\version" (
    set /p ver_val=<"src\data\version"
)

echo [93m
echo       _____          __  .__  .__          __  .__           ___________            .__          
echo      /  _  \________/  ^|_^|  ^| ^|__^| _______/  ^|_^|__^| ____     \__    ___/___   ____ ^|  ^|   ______ 
echo     /  /_\  \_  __ \   __\  ^| ^|  ^|/  ___/\   __\  ^|/  _ \      ^|    ^| /  _ \ /  _ \^|  ^|  /  ___/ 
echo    /    ^|    \  ^| \/^|  ^| ^|  ^|_^|  ^|\___ \  ^|  ^| ^|  ^|  ^<_^> )     ^|    ^|(  ^<_^> ^|  ^<_^> )  ^|__\___ \  
echo    \____^|__  /__^|   ^|__^| ^|____/__/____  ^> ^|__^| ^|__^|\____/      ^|____^| \____/ \____/^|____/____  ^> 
echo            \/                         \/                                                     \/  
echo                                     [96mAuthor: Mu_rpy[0m
echo                                     [92mVersion: %ver_val%[0m
echo.
echo [0m1. Stock Footage Downloader
echo 2. SFX / Music Downloader
echo 3. Install Latest Updates
echo 4. Exit
echo.

set "menu="
set /p menu="Select an option (1-4): "

if "%menu%"=="1" (
    pipenv run python src/artlistio-vid.py
    pause
    goto :run_script
)
if "%menu%"=="2" (
    pipenv run python src/artlistio-sfx.py
    pause
    goto :run_script
)
if "%menu%"=="3" (
    pipenv run python src/updater.py
    pause
    goto :run_script
)
if "%menu%"=="4" exit /b 0

goto :run_script