# [Aplikasi Manajemen Tagihan Keuangan]

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Django](https://img.shields.io/badge/Django-5.0-green.svg)
![Waitress](https://img.shields.io/badge/Server-Waitress-yellow.svg)

Aplikasi web berbasis Django yang dirancang untuk menampilkan, memfilter, dan mengelola data tagihan secara efisien. Proyek ini dibangun dengan arsitektur Server-Side Processing untuk menangani data dalam jumlah besar dengan cepat, dan disajikan menggunakan web server Waitress yang siap untuk produksi dengan database Microsoft SQL Server.

## Fitur Utama

-   **Tabel Data Interaktif:** Menampilkan data menggunakan jQuery DataTables yang responsif.
-   **Arsitektur Server-Side:** Semua proses filtering, sorting, dan paginasi dilakukan di sisi server untuk performa maksimal.
-   **Filter Lanjutan per Kolom:** Setiap kolom memiliki tombol filter kustom untuk menyaring data berdasarkan nilai-nilai unik.
-   **Filter Cascading Cerdas:** Opsi filter pada satu kolom secara otomatis menyesuaikan diri berdasarkan filter yang aktif di kolom lain.
-   **Sorting Kustom:** Pengguna dapat mengurutkan data berdasarkan abjad atau nilai (terkecil/terbesar) langsung dari modal filter.
-   **Deployment-Ready:** Menggunakan web server WSGI Waitress yang lebih andal daripada development server bawaan Django.

## Arsitektur & Teknologi

-   **Backend:**
    -   Python 3.x
    -   Django Framework
    -   Waitress (WSGI Server)
    -   `mssql-django` (Database Connector)
    -   `python-dotenv` (Manajemen Environment Variables)
-   **Frontend:**
    -   HTML5 / CSS3
    -   JavaScript (jQuery & DataTables.js)
    -   Bootstrap 5 (atau framework CSS lainnya)
-   **Database:**
    -   Microsoft SQL Server

---

## Prasyarat

Sebelum memulai, pastikan sistem Anda telah terinstal:
1.  **Python 3.8+** ([Download](https://www.python.org/downloads/)) - *PENTING: Centang "Add Python to PATH" saat instalasi di Windows.*
2.  **Git** ([Download](https://git-scm.com/downloads/)).
3.  **Microsoft ODBC Driver for SQL Server** ([Download](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)) - *Wajib agar Django bisa terhubung ke MS SQL Server.*

---

## Langkah-langkah Instalasi & Setup

Berikut adalah cara untuk menjalankan proyek ini di lingkungan lokal dari awal.

#### 1. Clone Repository
```bash
git clone https://github.com/arkandinov/django_data_exce_website.git
cd [nama-folder-repo]
```

### 2. Buat dan Aktifkan Virtual Environment
```bash
# Membuat virtual environment
python -m venv venv

# Mengaktifkan di Windows (CMD atau PowerShell yang sudah di-setting)
venv\Scripts\activate

# Mengaktifkan di macOS/Linux
source venv/bin/activate
```

### 3. Instal Semua Dependensi
Perintah ini akan menginstal semua paket yang terdaftar di requirements.txt ke dalam venv Anda.
```bash
pip install -r requirements.txt
```

### 4. Konfigurasi Environment (.env)
Ini adalah langkah paling penting untuk koneksi database dan keamanan.
```bash
# Django Core
SECRET_KEY='ganti-dengan-kunci-rahasia-anda'
DEBUG=True

# Konfigurasi Database (Microsoft SQL Server)
DB_ENGINE='databse_engine'
DB_NAME='NamaDatabaseAnda'
DB_USER='UsernameSQLAnda'
DB_PASSWORD='PasswordSQLAnda'
DB_HOST='AlamatIPAtauNamaServerSQL'
DB_PORT='1433'
DB_DRIVER='ODBC Driver 17 for SQL Server'
```
### 5. Tambahkan ip anda di settings.py dan run_waitress.py
Pastikan file settings.py Anda terdapat ip anda.
Cari kode ini di bagian atas file settings.py:
```bash
ALLOWED_HOSTS = ['ganti_dengan_ip_anda','localhost','127.0.0.1']
```
Pastikan file run_waitress.py Anda terdapat ip anda.
Cari kode ini di run_waitress.py:
```bash
if __name__ == '__main__':
    serve(application, host='ganti_dengan_ip_anda', port=5050)
```
### 6. Cara Menjalankan Aplikasi
Gunakan Waitress untuk menjalankan server. Pastikan venv Anda aktif.
```bash
# Ganti 'namaproyek' dengan nama folder konfigurasi Django Anda
waitress-serve --host=127.0.0.1 --port=8000 namaproyek.wsgi:application
```
