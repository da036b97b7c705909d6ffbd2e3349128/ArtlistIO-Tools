import asyncio
import os
import struct
import subprocess
from playwright.async_api import async_playwright

async def get_m3u8_link(target_url):
    arch = "64" if struct.calcsize("P") == 8 else "32"
    base_dir = os.path.dirname(os.path.abspath(__file__))
    chrome_path = os.path.join(base_dir, "dependencies", f"chrome-win{arch}", "chrome.exe")

    found_event = asyncio.Event()
    m3u8_url = None

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, executable_path=chrome_path)
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
            for task in [nav_task, wait_task]:
                if not task.done():
                    task.cancel()
            await browser.close()
            
    return m3u8_url

def convert_m3u8(url):
    base_path = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.normpath(os.path.join(base_path, "..", "output"))
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    ffmpeg_path = os.path.join(base_path, "dependencies", "ffmpeg", "bin", "ffmpeg.exe")
    name = input("Enter output filename: ").strip()

    if not name.endswith(".mp4"):
        name += ".mp4"

    output_file = os.path.join(output_dir, name)

    command = [
        ffmpeg_path,
        "-i", url,
        "-c", "copy",
        "-bsf:a", "aac_adtstoasc",
        output_file
    ]

    try:
        subprocess.run(command, check=True)
        print(f"Success: {output_file}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    target = input("Enter the website URL: ").strip()
    found_url = asyncio.run(get_m3u8_link(target))
    if found_url:
        convert_m3u8(found_url)
    else:
        print('Unable to retrieve m3u8 url.')