from playwright.sync_api import sync_playwright
# tambah watchdog untuk live reload
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os

url = input("Masukkan URL yang ingin dibuka: ").strip()
# dari_uipath = "D:\\porto\\BBB\\fmt\\jobportal\\surat_lamaran_PT Karya Solusi Prima.pdf"
# proses_uipath = Path(dari_uipath).resolve()
# filepath_uipath = str(proses_uipath)
# print(filepath_uipath)

filepath_uipath = r"D:\porto\BBB\fmt\jobportal\surat_lamaran_PT Karya Solusi Prima.pdf"
posisi_loker = "Relationship Officer"
nama_perusahaan = "PT BCA Finance"


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
        # user_data_dir=user_data_dir, #pakai chrome profile asli
        user_data_dir=user_data_dir,
        channel="chrome", # Use the branded Google Chrome
        headless=False
    )
    
    # Use the existing first page created by the persistent context
    # page = context.pages[0]
    page = context.new_page()
    page.goto(url, wait_until="domcontentloaded")

    # Mengatur timeout default untuk semua aksi di halaman tersebut menjadi 15 detik.
    # page.set_default_timeout(15000)

    # Khusus mengatur timeout untuk proses berpindah halaman/URL
    # page.set_default_navigation_timeout(15000)

    page.pause()

    # # Mendapatkan elemen posisi
    # posisi_locator = page.locator("h1[data-automation='job-detail-title']")
    # posisi_locator.wait_for(state="visible", timeout=5000)

    # # Ambil Text
    # posisi_loker = posisi_locator.inner_text()

    # # Mendapatkan elemen Nama Perusahaan
    # namaperusahaan_locator = page.locator("span[data-automation='advertiser-name']")
    # namaperusahaan_locator.wait_for(state="visible", timeout=5000)

    # # Ambil Text
    # nama_perusahaan = namaperusahaan_locator.inner_text()
    
    # Mendapatkan lokasi perusahaan berada
    lokasi_locator = page.locator('span[data-automation="job-detail-location"]')
    lokasi_locator.wait_for(state="visible", timeout=5000)

    # Ambil Teks
    lokasi_perusahaan = lokasi_locator.inner_text()

    # # Klik Lamar
    page.get_by_text("Lamaran Cepat").click(delay=2000)
    lokasi_locator.wait_for(state="visible", timeout=10000)

    # Pilih Upload Surat Lamaran
    ##### Works #1 - not works anymore

    # try:
    #     # 1. Pastikan area cover letter terbuka (biasanya klik opsi "Unggah" dulu)
    #     page.locator("label").filter(has_text="Unggah surat lamaran").click()
        
    #     # 2. LANGSUNG set_input_files ke locator yang tadi 'resolved' di call log
    #     # Jangan diklik lagi! Langsung tembak filenya.
    #     upload_locator = page.get_by_test_id("coverLetterFileInput").get_by_test_id("upload-button").get_by_test_id("file-input")
        
    #     upload_locator.wait_for(state="visible", timeout=5000)
    #     upload_locator.set_input_files(filepath_uipath)
        
    #     print("File berhasil diinput.")

    # except Exception as e:
    #     # Jika cara di atas gagal, gunakan 'Jurus Pamungkas' (input tersembunyi)
    #     print("Mencoba metode alternatif...")
    #     page.get_by_test_id("file-input").get_by_test_id("coverLetterFileInput").locator("input[type='file']").set_input_files(filepath_uipath)

    ##### end of works #1

    # # Works #2 - Lebih rapi - not works anymore
    # try:
    #     # 1. Aktifkan area cover letter
    #     page.locator("label").filter(has_text="Unggah surat lamaran").click(delay=2000)

    #     area_upload = page.get_by_test_id("coverLetterFileInput")
    #     area_upload.wait_for(state="visible", timeout=5000)

    #     # 2. Targetkan elemen input di dalam area tersebut
    #     input_file = area_upload.locator("input[type='file']").locator("input=[data-testid='file-input']")
        
    #     # 3. Masukkan file
    #     input_file.set_input_files(filepath_uipath)
    #     print("Berhasil! File telah terdeteksi oleh sistem.")

    # except Exception as e:
    #     print(f"Terjadi kesalahan: {e}")
    
    # end of works #2

    # Pilih tanpa surat lamaran
    page.locator('input[data-testid="coverLetter-method-none"]').click()
    
    # Pilih menulis surat Lamaran
    page.locator("label[for=':r15:']").click()

    # Menulis surat lamaran
    page.locator("textarea[data-testid='coverLetterTextInput']").click()

    # Menghapus surat lamaran lama
    page.locator("textarea[data-testid='coverLetterTextInput']").clear()

    # Menulis surat lamaran
    page.locator("textarea[data-testid='coverLetterTextInput']").fill("HRD yang terhormat, \n\nSaya, Eko Priambodo, tertarik melamar posisi"+" "+posisi_loker+" "+"di"+" "+nama_perusahaan+". Saya memiliki pengalaman selama 2 tahun di bidang administrasi, 3 tahun di IT Support serta memiliki keahlian dalam menggunakan Microsoft Office.")

    # set Gaji
    expected_salary = ""

    if any(loc in lokasi_perusahaan for loc in [ "Yogyakarta", "Semarang", "Kendal", "Batang" ]):
        expected_salary = "ID_Q_2588_V_2_A_2593"
    elif "Jakarta" in lokasi_perusahaan:
        expected_salary = "ID_Q_2588_V_2_A_2598"

    # Klik Lanjut
    page.locator('button[data-testid="continue-button"]').click(delay=2000)

    # Jawab Pertanyaan Gaji
    page.get_by_text("What's your expected monthly").select_option(expected_salary)
    page.locator('label[for="question-ID_Q_2588_V_2"]').select_option(expected_salary)

    # Klik Lanjut
    page.locator('button[data-testid="continue-button"]').click(delay=2000)

    # Klik Lanjut
    next_lamar = page.locator('button[data-testid="continue-button"]').click(delay=2000)
    next_lamar.wait_for(state="visible", timeout=5000)

    # Klik Lamar
    lamar = page.locator('button[data-testid="review-submit-application"]').click(delay=2000)
    lamar.wait_for(state="visible", timeout=5000)

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
