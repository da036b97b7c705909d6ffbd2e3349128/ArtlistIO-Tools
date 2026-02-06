import subprocess, os, time, sys, platform, re, struct
from playwright.sync_api import sync_playwright

arch = "64" if struct.calcsize("P") == 8 else "32"
base_dir = os.path.dirname(os.path.abspath(__file__))
CHROME_EXE_PATH = os.path.join(base_dir, "dependencies", f"chrome-win{arch}", "chrome.exe")
FFMPEG_PATH = os.path.abspath(os.path.join("ffmpeg", "bin", "ffmpeg.exe"))
AUDIO_DIR = os.path.normpath(os.path.join(base_path, "..", "output"))
os.makedirs(AUDIO_DIR, exist_ok=True)

def convert(aac_url, aac_name):
    latest_file = os.path.join(AUDIO_DIR, f"{aac_name}.mp3")
    if os.path.exists(latest_file):
        count = 1
        while os.path.exists(os.path.join(AUDIO_DIR, f"{aac_name}_{count}.mp3")):
            count += 1
        os.rename(latest_file, os.path.join(AUDIO_DIR, f"{aac_name}_{count}.mp3"))

    command = [
        FFMPEG_PATH, "-y", "-stats",
        "-i", aac_url,
        "-acodec", "libmp3lame",
        "-ab", "192k",
        latest_file
    ]

    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1, encoding='utf-8')
        for line in process.stdout:
            if "size=" in line or "time=" in line:
                sys.stdout.write(f"\rConverting: {line.strip()}")
                sys.stdout.flush()
        process.wait()
        print(f'\nSuccessfully created {latest_file}!')
    except Exception as e:
        print(f"\nFFMPEG failed: {e}")

def click_render_play_button(page):
    target_btn = page.locator("button[data-testid='renderButton']").filter(has_text="Play").first
    if target_btn.is_visible():
        target_btn.scroll_into_view_if_needed()
        target_btn.click(force=True)
        return True
    return False

def get_aac_data(target_url):
    if not os.path.exists(CHROME_EXE_PATH):
        print(f"BRAVE NOT FOUND AT: {CHROME_EXE_PATH}")
        return None, None

    aac_link = None
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROME_EXE_PATH, headless=True)
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        def handle_request(request):
            nonlocal aac_link
            if ".aac" in request.url.lower() and not aac_link:
                aac_link = request.url

        page.on("request", handle_request)

        try:
            print("Extracting raw audio...")
            page.goto(target_url, wait_until="domcontentloaded", timeout=60000)
            time.sleep(2)
            click_render_play_button(page)

            for _ in range(10):
                if aac_link: break
                time.sleep(0.5)
                
        except Exception as e:
            print(f"Browser Error: {e}")

        match = re.search(r'track/(.*?)/', target_url)
        text_inside = match.group(1)

        browser.close()
        return aac_link, text_inside

def config(url):
    url = url.strip()
    link, name = get_aac_data(url)
    if link:
        convert(link, name)
        return True
    else:
        raise Exception("Failed to find link.")

def debug_mode():
    while True:
        url = input("\nEnter a URL: ").strip()
        if not url: continue
        link, name = get_aac_data(url)
        if link:
            print(name)
            print('file extracted!')
        else:
            print("Failed to find link.")

if __name__ == "__main__":
    config(input('Enter a URL: '))