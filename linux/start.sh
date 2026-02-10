#!/bin/bash

G='\e[92m'; C='\e[96m'; Y='\e[93m'; R='\e[0m'

mkdir -p output/videos

if [ ! -f "src/data/.setup_done" ]; then
    clear
    [ -f "src/data/LICENSE" ] && cat "src/data/LICENSE"
    echo ""
    read -p "Do you accept the license terms? (y/n): " choice
    [[ ! "$choice" =~ ^[Yy]$ ]] && exit 0

    echo "[PHASE 1] Verifying system requirements..."
    command -v pipenv >/dev/null || pip install --user pipenv

    if ! command -v ffmpeg >/dev/null; then
        echo "ffmpeg not found. Please install it via your package manager (e.g., sudo pacman -S ffmpeg)"
        exit 1
    fi

    echo "[PHASE 2] Configuring Python dependencies..."
    pipenv install
    
    echo "[PHASE 3] Installing browser dependencies..."
    pipenv run python -m playwright install chromium
    pipenv run python -m playwright install-deps chromium
    
    echo "[PHASE 4] Verifying integrity of files..."
    pipenv run python src/integrity.py
    if [ $? -ne 0 ]; then
        echo -e "\e[91m[CRITICAL] Integrity check failed.\e[0m"
        read -p "Continue anyway? (Experimental Build) (y/n): " cont
        if [[ ! $cont =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi    
    touch src/data/.setup_done
fi

clear
VER=$(cat src/data/version 2>/dev/null || echo "Unknown")

echo -e "${Y}"
echo "    _____          __  .__  .__          __  .___________    ___________            .__          "
echo "   /  _  \________/  |_|  | |__| _______/  |_|   \_____  \   \__    ___/___   ____ |  |  ______ "
echo "  /  /_\  \_  __ \   __\  | |  |/  ___/\   __\   |/   |   \    |    | /  _ \ /  _ \|  |  /  ___/ "
echo " /    |    \  | \/|  | |  |_|  |\___ \  |  | |   /    |    \   |    |(  <_> |  <_> )  |__\___ \  "
echo " \____|__  /__|   |__| |____/__/____  > |__| |___\_______  /   |____| \____/ \____/|____/____  "
echo "         \/                         \/                   \/                                  \/  "
echo -e "${R}"

echo -e "                                     ${C}Author: Mu_rpy${R}"
echo -e "                                     ${G}Version: $VER${R}\n"

echo "1. Stock Footage Downloader"
echo "2. SFX / Music Downloader"
echo "3. Install Latest Updates"
echo "4. Exit"
echo ""

read -p "Select an option (1-4): " menu
case $menu in
    1) pipenv run python src/artlistio-vid.py ;;
    2) pipenv run python src/artlistio-sfx.py ;;
    3) pipenv run python src/updater.py ;;
    4) exit 0 ;;
    *) echo "Invalid selection"; sleep 2; ./start.sh ;;
esac