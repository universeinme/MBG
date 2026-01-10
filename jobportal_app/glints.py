from playwright.sync_api import sync_playwright
# tambah watchdog untuk live reload
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os

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
user_data_dir=os.path.join(os.getcwd(), "playwright")

with sync_playwright() as p:
    # Launch persistent context
    context = p.chromium.launch_persistent_context(
        user_data_dir=user_data_dir,
        channel="chrome", # Use the branded Google Chrome
        headless=False
    )
    
    page = context.new_page()
    page.goto(url, wait_until="domcontentloaded")

    page.pause()

    # 1. Klik Tombol Lamar
    page.get_by_role("main").get_by_role("button", name="Lamar", exact=True).click()

    # 2. Pilih cv
    page.get_by_role("button", name="Selanjutnya").click()

    # 3. Menjawab Pertanyaan
    # a. populate label
    label_ahli = page.locator("label").filter(has_text="Ahli")
    label_ahli.first.wait_for(state="visible")

    # b Iterasi klik
    for label in label_ahli.all():
        label.click()

    # c. Klik Selanjutnya
    page.get_by_role("button", name="Selanjutnya").click()

    # Bagian Jumlah seksi pertanyaannya random, based on siapa yang posting loker, range 3-11 bahkan lebih
    # disini bagian iterasinya


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
