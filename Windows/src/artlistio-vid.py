import asyncio
import re
import os
import subprocess
from playwright.async_api import async_playwright

async def get_m3u8_link(target_url):
    found_event = asyncio.Event()
    m3u8_url = None

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        def handle_request(request):
            nonlocal m3u8_url
            if ".m3u8" in request.url:
                m3u8_url = request.url
                found_event.set()

        page.on("request", handle_request)

        try:
            nav_task = asyncio.create_task(page.goto(target_url, wait_until="domcontentloaded"))
            wait_task = asyncio.create_task(found_event.wait())
            
            await asyncio.wait([nav_task, wait_task], return_when=asyncio.FIRST_COMPLETED)

            if not found_event.is_set():
                for _ in range(2):
                    await page.mouse.wheel(0, 2000)
                    try:
                        await asyncio.wait_for(found_event.wait(), timeout=3)
                        break
                    except asyncio.TimeoutError:
                        continue
        finally:
            await browser.close()
            
    return m3u8_url

def download_with_streamlink(url, target_url):
    output_dir = os.path.normpath(os.path.join(os.getcwd(), "output", "videos"))
    os.makedirs(output_dir, exist_ok=True)

    match = re.search(r'/(?:song|track|sfx|clip)/(.*?)/(?:\d+)', target_url)
    default_name = match.group(1).split('/')[-1] if match else "latest"

    name = input(f"Enter output filename (default: {default_name}.mp4): ").strip()
    if not name: 
        name = default_name
    
    if not name.lower().endswith(".mp4"):
        name += ".mp4"
    
    output_file = os.path.join(output_dir, name)
    ffmpeg_exe = os.path.abspath(os.path.join(os.path.dirname(__file__), "ffmpeg.exe"))

    command = [
        "streamlink",
        "--ffmpeg-ffmpeg", ffmpeg_exe,
        url, "best",
        "-o", output_file,
        "--force"
    ]

    try:
        subprocess.run(command, check=True)
        print(f"\n[SUCCESS] Video saved to: {output_file}")
    except Exception as e:
        print(f"\n[ERROR] Streamlink failed: {e}")

if __name__ == "__main__":
    target = input("Enter Artlist Video URL: ").strip()
    if target:
        print("[INFO] Searching for stream...")
        found_url = asyncio.run(get_m3u8_link(target))
        if found_url:
            print("[INFO] Stream found. Starting download...")
            download_with_streamlink(found_url, target)
        else:
            print("[ERROR] Could not find video stream.")