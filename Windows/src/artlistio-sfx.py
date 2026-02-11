import subprocess, os, time, sys, re
from playwright.sync_api import sync_playwright

base_dir = os.path.dirname(os.path.abspath(__file__))
# Points to the ffmpeg.exe downloaded by your start.bat
FFMPEG_PATH = os.path.abspath(os.path.join(base_dir, "ffmpeg.exe"))
AUDIO_DIR = os.path.normpath(os.path.join(base_dir, "..", "output", "audio"))
os.makedirs(AUDIO_DIR, exist_ok=True)

def convert(aac_url, aac_name):
    latest_file = os.path.join(AUDIO_DIR, f"{aac_name}.mp3")
    
    # Extension logic
    if not latest_file.lower().endswith(".mp3"):
        latest_file += ".mp3"

    command = [
        FFMPEG_PATH, "-y", "-i", aac_url,
        "-acodec", "libmp3lame", "-ab", "192k",
        latest_file
    ]

    try:
        subprocess.run(command, check=True, capture_output=True)
        print(f'\n[SUCCESS] Created {latest_file}')
    except Exception as e:
        print(f"\n[ERROR] FFMPEG failed: {e}")

def click_render_play_button(page):
    try:
        target_btn = page.locator("button[data-testid='renderButton']").filter(has_text="Play").first
        if target_btn.is_visible():
            target_btn.click(force=True)
            return True
    except:
        pass
    return False

def get_aac_data(target_url):
    aac_link = None
    with sync_playwright() as p:
        # Removed hardcoded executable_path; uses playwright's chromium
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        def handle_request(request):
            nonlocal aac_link
            if ".aac" in request.url.lower() and not aac_link:
                aac_link = request.url

        page.on("request", handle_request)

        try:
            print("[INFO] Extracting raw audio...")
            page.goto(target_url, wait_until="domcontentloaded", timeout=60000)
            time.sleep(2)
            click_render_play_button(page)

            for _ in range(10):
                if aac_link: break
                time.sleep(0.5)
        except Exception as e:
            print(f"[ERROR] Browser Error: {e}")

        match = re.search(r'/(?:song|track|sfx)/(.*?)/(?:\d+)', target_url)
        text_inside = match.group(1).split('/')[-1] if match else "latest"

        browser.close()
        return aac_link, text_inside

def config(url):
    url = url.strip()
    if not url: return
    link, name = get_aac_data(url)
    if link:
        convert(link, name)
    else:
        print("[ERROR] Failed to find audio link.")

if __name__ == "__main__":
    url_input = input('Enter Artlist SFX/Music URL: ')
    config(url_input)