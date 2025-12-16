📚 Sistem Perpustakaan Mini - Barcode Dinamis (Offline)

Aplikasi manajemen perpustakaan mandiri yang dikembangkan menggunakan Python dan Streamlit. Proyek ini mendigitalisasi proses peminjaman dan pengembalian buku dengan memanfaatkan teknologi Barcode Dinamis sebagai kunci verifikasi transaksi.

📝 Deskripsi Aplikasi

Aplikasi ini hadir sebagai solusi bagi perpustakaan skala kecil untuk mengelola inventaris secara akurat. Menggunakan sistem penyimpanan CSV 100% offline, menjamin keamanan data lokal tanpa memerlukan server atau koneksi internet.

Fitur Utama:

    TRX-ID Dinamis: Setiap peminjaman menghasilkan Barcode unik (Code 128) sebagai bukti transaksi.

    Automasi Stok: Update stok otomatis (tambah/kurang) melalui pemindaian Barcode via webcam.

    Dashboard Statistik: Visualisasi stok dan transaksi secara real-time dengan tema Tembaga.

🚀 Cara Menjalankan Aplikasi

    Pastikan Python terinstal (Versi 3.9 atau lebih baru).

    Instal library yang dibutuhkan melalui terminal/CMD:
    Bash

pip install streamlit pandas python-barcode pyzbar pillow plotly

Persiapkan Direktori: Pastikan folder data/ dan qr/ sudah tersedia di folder proyek.

Jalankan Aplikasi:
Bash

    streamlit run app.py

📂 Struktur Folder
Plaintext

/perpus_mini 

│─ app.py           
│─ utils.py

│─ qr/

│─ data/
│   
│
├── master.csv

│ ├── log.csv 

│ ├──backup/

│ └──laporan/

  

----------------------------------------------------------------------------------------------------------------------------------------

📸 Screenshot Aplikasi
<img width="1919" height="983" alt="image" src="https://github.com/user-attachments/assets/926a18b3-1ea6-4437-8722-6a5ea7d5e80d" />
<img width="1919" height="968" alt="Screenshot 2025-12-16 202634" src="https://github.com/user-attachments/assets/866abaf7-beac-41bc-9f77-a15446dd9080" />


	
🛠️ Penjelasan Fitur Utama
1. Manajemen Data (CRUD)

Aplikasi mendukung pengelolaan data buku secara terstruktur (Non-OOP):

    Create: Menambah buku baru ke database CSV.

    Read: Menampilkan tabel inventaris secara real-time.

    Update: Mengedit detail buku atau stok secara otomatis/manual.

    Delete: Menghapus data buku dari sistem secara permanen.

2. Barcode Dinamis (Code 128)

    Generasi: Saat peminjaman, sistem membuat TRX-ID unik yang diubah menjadi gambar Barcode.

    Verifikasi: Saat pengembalian, Barcode di-scan via webcam untuk memvalidasi transaksi di log.csv, mengubah status menjadi 'Kembali', dan menambah stok di master.csv.

👥 Pembagian Tugas

    [Nama Anda]: Pengembangan Logika Backend (utils.py), Integrasi Barcode, dan Pengolahan Data CSV.

    [Rekan Anda]: Pengembangan UI Streamlit (app.py), Visualisasi Dashboard, dan Penyusunan Dokumentasi.
