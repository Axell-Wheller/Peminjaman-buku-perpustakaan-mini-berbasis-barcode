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
<img width="1919" height="912" alt="image" src="https://github.com/user-attachments/assets/d8fac37a-46ec-4b1e-859c-1c71dcc5e606" />
<img width="1919" height="914" alt="image" src="https://github.com/user-attachments/assets/336c295c-52ef-4882-919e-e5569abb9a9a" />


	
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

    [Seiji Lian Wibowo, Zahra Aulia Junita, Nabila Maylani putri]: Pengembangan Logika Backend (utils.py),Integrasi Barcode, dan Pengolahan Data CSV.

    [Seiji Lian Wibowo & Riska Nabila]: Pengembangan UI Streamlit (app.py), Visualisasi Dashboard, dan Penyusunan Dokumentasi serta Laporan.
