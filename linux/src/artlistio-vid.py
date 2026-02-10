import asyncio
import os
import subprocess
import json
from playwright.async_api import async_playwright

async def get_m3u8_link(target_url):
    found_event = asyncio.Event()
    m3u8_url = None

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
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
            for task in [nav_task, wait_task]:
                if not task.done():
                    task.cancel()
            await browser.close()
            
    return m3u8_url

def convert_m3u8(url):
    base_path = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.normpath(os.path.join(base_path, "..", "output", "videos"))
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Force valid filename
    name = ""
    while not name:
        name = input("Enter output filename: ").strip()
    
    if not name.endswith(".mp4"):
        name += ".mp4"

    output_file = os.path.join(output_dir, name)

    try:
        # Fetch stream metadata via JSON
        result = subprocess.run(["streamlink", "--json", url], capture_output=True, text=True)
        stream_data = json.loads(result.stdout)
        streams = list(stream_data.get("streams", {}).keys())

        if not streams:
            print("Error: No available streams found for this URL.")
            return

        print(f"Available streams: {', '.join(streams)}")
        
        quality = ""
        while quality not in streams:
            quality = input("Select quality: ").strip()
            if quality not in streams:
                print(f"Invalid quality. Please choose from: {', '.join(streams)}")

        command = [
            "streamlink",
            "--stream-segment-threads", "10",
            "-o", output_file,
            url,
            quality
        ]

        # Subprocess will inherit stdout/stderr, showing the [cli][info] logs
        subprocess.run(command, check=True)
        print(f"Success: {output_file}")
    except Exception as e:
        print(f"Error during stream selection or download: {e}")

if __name__ == "__main__":
    target = ""
    while not target:
        target = input("Enter the website URL: ").strip()
    
    found_url = asyncio.run(get_m3u8_link(target))
    if found_url:
        convert_m3u8(found_url)
    else:
        print('Unable to retrieve m3u8 url.')