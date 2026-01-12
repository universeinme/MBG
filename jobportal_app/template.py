from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
# tambah watchdog untuk live reload
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os
import random

url = input("Masukkan URL yang ingin dibuka: ").strip()

class ReloadOnChange(FileSystemEventHandler):
    def __init__(self, page):
        self.page = page
        self.last_reload = 0

    def on_modified(self, event):
        if not event.src_path.endswith(".py"):
            return

        now = time.time()
        if now - self.last_reload > 1:
            print("Reload browser")
            self.page.reload()
            self.last_reload = now

# Base directory for all Chrome user data
user_data_dir=os.path.join(os.getcwd(), "browser")
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/109.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15"
]

with sync_playwright() as p:
    # Launch persistent context
    context = p.chromium.launch_persistent_context(
        user_data_dir=user_data_dir,
        channel="chrome", # Use the branded Google Chrome
        user_agent=random.choice(user_agents),
        headless=False
    )
    
    page = context.new_page()
    stealth_sync(page)
    page.goto(url, wait_until="domcontentloaded")

    page.pause()


    def on_close():
        print("Browser ditutup → program berhenti")
        observer.stop()
        sys.exit(0)

    context.on("close", on_close)

    observer = Observer()
    observer.schedule(ReloadOnChange(page), ".", recursive=True)
    observer.start()

    print("Watching file changes... (Ctrl+C to stop)")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
