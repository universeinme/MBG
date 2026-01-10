# MBG
Singkatan dari Mari Bekerja Guys.

Dibuat untuk membantu para pencaker seperti si pembuat biar banyak acara lainnya yang bisa ke handel.

**Fitur:**

- Mengirim email
- Submit lamaran kerja di jobstreet cukup dengan link jobstreet

## Arsitektur

### Python Engine
- Python 3.8
### Python Library
- Yagmail
- Keyring
- pytest-playwright
- watchdog

## Setup
### Email (Gmail Only)
- Perlu App Password, [referensi ](https://support.google.com/accounts/answer/185833)
- Username gmail dan Password: App password
- Set Environment username dan app password di level OS, bukan di project.
- Generate Keyring

### UiPath Package
- UiPath Excel
- UiPath Form
- UiPath Python
- UiPath System
- UiPath Word
- UiPath UIAutomation

### Browser untuk Playwright
- Kalau sudah terinstall chrome, cukup pake chrome. Config di playwright **channel="chrome"** ~~playwright install.~~
- Gunakan persisten context, biar ga login terus dan chrome profile khusus agar persisten context dapat tertampung.
- Agar tidak buka tutup browser dan cukup mengganti url-nya saja, maka menggunakan **connect_over_cdp** dengan catatan chrome telah terbuka dengan mode remote-debugging.

### Word Scope
- Agar template tidak teroverwrite, matikan autosave, jika tidak matikan autosave, gunakan save as dokumen activity untuk save a copy setelah load template.