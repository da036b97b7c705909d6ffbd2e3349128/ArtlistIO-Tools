import subprocess, os, time, sys, re
from playwright.sync_api import sync_playwright

base_dir = os.path.dirname(os.path.abspath(__file__))
# Updated for Linux structure
AUDIO_DIR = os.path.normpath(os.path.join(base_dir, "..", "output", "audio"))
os.makedirs(AUDIO_DIR, exist_ok=True)

def convert(aac_url, aac_name):
    latest_file = os.path.join(AUDIO_DIR, f"{aac_name}.mp3")
    
    if os.path.exists(latest_file):
        count = 1
        while os.path.exists(os.path.join(AUDIO_DIR, f"{aac_name}_{count}.mp3")):
            count += 1
        latest_file = os.path.join(AUDIO_DIR, f"{aac_name}_{count}.mp3")

    # Use ffmpeg for direct file download and conversion on Linux
    command = [
        "ffmpeg", "-y", "-i", aac_url,
        "-acodec", "libmp3lame",
        "-ab", "192k",
        latest_file
    ]

    try:
        print(f"Downloading and converting: {aac_name}...")
        subprocess.run(command, check=True, capture_output=True)
        print(f'Successfully created {latest_file}!')
    except Exception as e:
        print(f"\nConversion failed: {e}")

def click_render_play_button(page):
    target_btn = page.locator("button[data-testid='renderButton']").filter(has_text="Play").first
    if target_btn.is_visible():
        target_btn.scroll_into_view_if_needed()
        target_btn.click(force=True)
        return True
    return False

def get_aac_data(target_url):
    aac_link = None
    with sync_playwright() as p:
        # Launch using the binaries installed via start.sh
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
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

        match = re.search(r'/(?:song|track|sfx)/(.*?)/(?:\d+)', target_url)
        if match:
            text_inside = match.group(1).split('/')[-1]
        else:
            text_inside = "latest"

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

if __name__ == "__main__":
    config(input('Enter a URL: '))