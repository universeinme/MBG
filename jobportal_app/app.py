import os

def run_job(url,base_perusahaan,base_posisi):

    # filepath_uipath = os.path.normpath(dari_uipath)

    nama_perusahaan = str(base_perusahaan)
    nama_posisi = str(base_posisi)
    
    # 1. Impor Playwright secara dinamis (tanpa 'from ... import')
    pw_module = __import__('playwright.sync_api', fromlist=['sync_api'])
    
    # 2. Aktifkan Mode Debug/Inspeksi melalui environment variable
    # Ini akan memunculkan jendela "Playwright Inspector" otomatis
    # os.environ["PWDEBUG"] = "1"

    # 3. Start Playwright engine secara manual
    # p = pw_module.sync_api.sync_playwright().start()
    p = pw_module.sync_playwright().start()

    try:
        # Gunakan folder profil terpisah agar tidak bentrok dengan Chrome yang sedang terbuka
        # Playwright tidak bisa debug jika profil sedang dipakai aplikasi lain
        # user_data_dir = os.path.join(os.getcwd(), "playwright")

        # Launch persistent context
        # Mode headless otomatis False jika PWDEBUG=1, tapi kita set eksplisit agar aman
        
        # context = p.chromium.launch_persistent_context(
        #     user_data_dir=os.path.join(os.getcwd(), "playwright"),
        #     channel="chrome",
        #     headless=False
        #     # args=[f"--profile-directory=playwright"]
        # )

        # Agar tidak buka tutup browser dan cukup mengganti url-nya saja, maka menggunakan connect_over_cdp
        browser = p.chromium.connect_over_cdp("http://localhost:9222")

        context = browser.contexts[0]
        # Ambil halaman pertama yang otomatis terbuka
        page = context.pages[0]

        # Navigasi ke URL
        page.goto(url, wait_until="domcontentloaded")

        # Mendapatkan Elemen lokasi Perusahaan
        lokasi_locator = page.locator('span[data-automation="job-detail-location"]')
        lokasi_locator.wait_for(state="visible", timeout=5000)

        # Ambil Teks
        lokasi_perusahaan = lokasi_locator.inner_text()

        # Klik Lamar
        page.get_by_text("Lamaran Cepat").click()
        # lokasi_locator.wait_for(state="visible", timeout=5000)

        # # Upload surat lamaran
        # try:
        #     # 1. Aktifkan elemen cover letter
        #     page.locator("label").filter(has_text="Unggah surat lamaran").click(delay=2000)

        #     area_upload = page.get_by_test_id("coverLetterFileInput")
        #     area_upload.wait_for(state="visible", timeout=10000)

        #     # 2. Targetkan elemen input di dalam area tersebut
        #     input_file = area_upload.locator("input[type='file']")
            
        #     # 3. Masukkan file
        #     input_file.set_input_files(filepath_uipath)
        #     print("Berhasil! File telah terdeteksi oleh sistem.")

        # except Exception as e:
        #     print(f"Terjadi kesalahan: {e}")
            
        # Pilih tanpa surat lamaran
        # page.locator('input[data-testid="coverLetter-method-none"]').click()
        page.locator("label").filter(has_text="Jangan sertakan surat lamaran").click()
        # tanpa_suratlamaran.wait_for(state="visible", timeout=5000)

        # Pilih menulis surat Lamaran
        page.locator("label[for=':r15:']").click()

        # Menulis surat lamaran
        page.locator("textarea[data-testid='coverLetterTextInput']").click()

        # Menghapus surat lamaran lama
        page.locator("textarea[data-testid='coverLetterTextInput']").clear()

        # Menulis surat lamaran
        page.locator("textarea[data-testid='coverLetterTextInput']").fill("HRD yang terhormat, \n\nSaya, Eko Priambodo, tertarik melamar posisi"+" "+nama_posisi+" "+"di"+" "+nama_perusahaan+". Saya memiliki pengalaman selama 2 tahun di bidang administrasi, 3 tahun di IT Support serta memiliki keahlian dalam menggunakan Microsoft Office.")

        # Klik Lanjut
        page.locator('button[data-testid="continue-button"]').click()
        # setelah_surat.wait_for(state="visible", timeout=5000)

        # Set Gaji based on Lokasi Perusahaan
        expected_salary = ""

        if any(loc in lokasi_perusahaan for loc in [ "Yogyakarta", "Semarang", "Kendal", "Tegal", "Batang" ]):
            expected_salary = "ID_Q_2588_V_2_A_2593"
        elif "Jakarta" in lokasi_perusahaan:
            expected_salary = "ID_Q_2588_V_2_A_2598"

        # Jawab Pertanyaan Gaji
        page.get_by_text("What's your expected monthly").select_option(expected_salary)
        page.locator('label[for="question-ID_Q_2588_V_2"]').select_option(expected_salary)

        # Jawab Pertanyaan Pengalaman
        page.get_by_text("pengalaman").select_option("ID_Q_C006FC1023A280D20E3CC1C0588D2F6F_V_2_A_C006FC1023A280D20E3CC1C0588D2F6F_4")
        page.locator('label[for="question-ID_Q_C006FC1023A280D20E3CC1C0588D2F6F_V_2"]').select_option("ID_Q_C006FC1023A280D20E3CC1C0588D2F6F_V_2_A_C006FC1023A280D20E3CC1C0588D2F6F_4")

        # Klik Lanjut
        jawab_pertanyaan = page.locator('button[data-testid="continue-button"]').click()
        # jawab_pertanyaan.wait_for(state="visible", timeout=10000)

        # Klik Lanjut
        next_lamar = page.locator('button[data-testid="continue-button"]').click()
        # next_lamar.wait_for(state="visible", timeout=10000)

        # Klik Lamar
        lamar = page.locator('button[data-testid="review-submit-application"]').click()
        # lamar.wait_for(state="visible", timeout=10000)

        # Di return ke uipath
        return "Berhasil Melamar Loker"

        # 7. Cleanup manual (sangat penting karena tidak pakai 'with')
        if 'context' in locals():
            browser.close()
        p.stop()

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
