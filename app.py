import streamlit as st
import pandas as pd
from utils import *
import os
import time
import base64
import plotly.express as px 
from datetime import datetime

# --- TEMA CERAH: BIRU LANGIT + ABU-ABU ---
ACCENT_COLOR = "#2196F3"      # biru langit untuk aksen (garis, tombol, link)
BACKGROUND_COLOR = "#E3F2FD"  # biru langit sangat muda (background utama)
SIDEBAR_BG = "#F5F5F5"        # abu-abu muda untuk sidebar
TEXT_DARK = "#263238"         # abu-abu gelap untuk teks
CARD_BG = "#FFFFFF"        # background putih untuk kartu/form


# --- INJEKSI CSS UNTUK TAMPILAN BARU ---
st.set_page_config(
    page_title="Sistem Perpustakaan", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

st.markdown(f"""
<style>

/* ================== GLOBAL BACKGROUND ================== */

/* Pastikan semua area utama pakai background biru muda */
html, body, [data-testid="stAppViewContainer"] {{
    background-color: {BACKGROUND_COLOR};
}}

.main {{
    background-color: {BACKGROUND_COLOR};
}}

/* Hilangkan background header default biar nyatu */
[data-testid="stHeader"] {{
    background-color: rgba(0, 0, 0, 0);
}}

/* ================== SIDEBAR ================== */

[data-testid="stSidebar"] {{
    background-color: {SIDEBAR_BG};      /* abu-abu muda */
    color: {TEXT_DARK};
    font-size: 16px;
    border-right: 1px solid #E0E0E0;
}}

.stRadio > label > div {{
    color: {TEXT_DARK};
    font-weight: 500;
}}

/* ================== KONTEN / CARD ================== */

.block-container {{
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}}

/* Tombol utama (logout, submit, dll) */
div.stButton > button:first-child {{
    background-color: {ACCENT_COLOR};
    color: #FFFFFF;
    border: none;
    border-radius: 8px;
    height: 3em;
    font-weight: 600;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
}}

div.stButton > button:hover {{
    background-color: #1976D2;   /* biru sedikit lebih gelap saat hover */
    border: none;
}}

/* ================== JUDUL & TEKS ================== */

h1 {{
    color: #0D47A1;                             /* biru tua */
    font-size: 2.4em;
    border-bottom: 3px solid {ACCENT_COLOR};    /* garis biru langit */
    padding-bottom: 6px;
    margin-bottom: 1rem;
}}

h2, h3, h4 {{
    color: {TEXT_DARK};
}}

p, label, span {{
    color: {TEXT_DARK};
}}

/* ================== LINK ================== */

a {{
    color: {ACCENT_COLOR} !important;
    text-decoration: none;
}}
a:hover {{
    text-decoration: underline;
}}

/* Sembunyikan tombol Deploy di kanan atas */
.stDeployButton {{
    visibility: hidden;
}}

/* Bungkus form (seperti di Tambah Buku) jadi kartu putih */
div[data-testid="stForm"] {{
    background-color: {CARD_BG};
    border-radius: 12px;
    padding: 1.5rem 1.8rem;
    box-shadow: 0 2px 10px rgba(15, 23, 42, 0.12);
}}

/* Biar input, number input, dan text area tetap putih dan teks gelap */
input, textarea {{
    background-color: #FFFFFF !important;
    color: {TEXT_DARK} !important;
}}

/* Beberapa komponen input Streamlit pakai baseweb */
div[data-baseweb="input"] > input {{
    background-color: #FFFFFF !important;
    color: {TEXT_DARK} !important;
}}

div[data-baseweb="textarea"] > textarea {{
    background-color: #FFFFFF !important;
    color: {TEXT_DARK} !important;
}}

/* Label di atas field jangan terlalu pucat */
label {{
    color: {TEXT_DARK} !important;
    font-weight: 500;
}}

/* ====== PERJELAS KOTAK INPUT (Login + form lain) ====== */

/* Wrapper input (text / password / number) */
div[data-baseweb="input"] {{
    background-color: #FAFAFA !important;        /* abu-abu sangat muda */
    border-radius: 8px;
    border: 1px solid #CFD8DC;                   /* garis abu-abu */
    padding: 0.25rem 0.75rem;
}}

/* Teks di dalam input */
div[data-baseweb="input"] input {{
    background-color: transparent !important;    /* biar ikut warna wrapper */
    color: {TEXT_DARK} !important;               /* teks gelap */
}}

/* Text area (kalau ada) */
div[data-baseweb="textarea"] {{
    background-color: #FAFAFA !important;
    border-radius: 8px;
    border: 1px solid #CFD8DC;
    padding: 0.25rem 0.75rem;
}}

div[data-baseweb="textarea"] textarea {{
    background-color: transparent !important;
    color: {TEXT_DARK} !important;
}}

/* Label di atas field */
label {{
    color: {TEXT_DARK} !important;
    font-weight: 500;
}}


</style>
""", unsafe_allow_html=True)



# --- INISIALISASI SESSION STATE UNTUK LOGIN ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = None
if 'role' not in st.session_state: 
    st.session_state['role'] = None
# ---------------------------------------------


# FUNGSI HELPER
# Menggunakan ACCENT_COLOR untuk link download
def get_image_download_link(filepath, filename, text):
    if not os.path.exists(filepath):
        return ""
    with open(filepath, "rb") as image_file:
        base64_img = base64.b64encode(image_file.read()).decode()
    href = f'<a href="data:file/png;base64,{base64_img}" download="{filename}" style="color: {ACCENT_COLOR}; text-decoration: none;">{text}</a>'
    return href

def get_binary_file_downloader_html(bin_file, file_label='File'):
    if not os.path.exists(bin_file):
        return ""
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}" style="color: {ACCENT_COLOR}; text-decoration: none;">{file_label}</a>'
    return href

# --- PRE-CHECK: PASTIKAN FOLDER ADA ---
os.makedirs('data/laporan', exist_ok=True)
os.makedirs('data/backup', exist_ok=True)
os.makedirs('qr', exist_ok=True)
# -------------------------------------

# --- IMPLEMENTASI LOGIN ---
if not st.session_state['logged_in']:
    st.sidebar.title(" Login Pengguna")
    st.sidebar.info("Username/Password: admin/12345 atau kasir/abcde") 
    
    with st.sidebar.form("Login Form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            sukses, role = otentikasi_user(username, password) 
            if sukses:
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.session_state['role'] = role 
                st.success(f"Selamat datang, {username} ({role.upper()})!")
                st.rerun()
            else:
                st.error("Username atau Password salah.")
    st.stop()
# -------------------------------------

# Logout Button
if st.sidebar.button("Keluar (Logout)"):
    st.session_state['logged_in'] = False
    st.session_state['username'] = None
    st.session_state['role'] = None 
    st.rerun()

# Navigasi Menu
menu = st.sidebar.radio("Navigasi", ["Dashboard ", "Manajemen Buku (CRUD) ", "Scanner Barcode ", "Log Peminjaman & Laporan ", "Pengaturan & Backup ", "Tentang"])


# MENU 1: DASHBOARD
if menu == "Dashboard ":
    st.title(" Dasbor Ringkasan Perpustakaan")
    
    total_buku, total_trx, dipinjam_saat_ini = ringkasan_data_dasbor()
    
    st.markdown("### Statistik Utama")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Koleksi Unik", total_buku)
    col2.metric("Total Transaksi Tercatat", total_trx)
    col3.metric("Sedang Dipinjam Saat Ini", dipinjam_saat_ini)
    
    st.subheader("Distribusi Stok Berdasarkan Pengarang")
    df_master = muat_data_buku()
    
    if not df_master.empty:
        df_stok_pengarang = df_master.groupby('pengarang')['stok'].sum().reset_index()
        fig = px.bar(df_stok_pengarang, 
                     x='pengarang', y='stok', 
                     title="Total Stok per Pengarang",
                     color='pengarang')
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Catatan Transaksi Terbaru")
        st.dataframe(get_log_terbaru(10), use_container_width=True)


# MENU 2: CRUD
elif menu == "Manajemen Buku (CRUD) ":
    st.title(" Data Master Buku (CRUD)")
    
    is_admin = st.session_state['role'] == 'admin'
    
    if is_admin:
        tab_list = ["Tambah Buku", "Update Data", "Tabel Master", "Hapus Data"]
    else: 
        tab_list = ["Tabel Master", "Hapus Data"] 
        st.warning("Akses Tambah dan Update dibatasi hanya untuk Administrator.")
    
    tabs = st.tabs(tab_list)

    # --- TAB TAMBAH BUKU (Hanya Admin) ---
    if "Tambah Buku" in tab_list:
        with tabs[tab_list.index("Tambah Buku")]:
            st.subheader("Formulir Penambahan Koleksi Baru")
            with st.form("form_tambah_buku"):
                col_id, col_judul = st.columns(2)
                id_b = col_id.text_input("ID Buku (Cth: A001)", help="Wajib unik").upper() 
                jdl = col_judul.text_input("Judul Buku")
                pgr = st.text_input("Pengarang") 
                stk = st.number_input("Jumlah Stok", min_value=1, value=1)
                
                if st.form_submit_button(" Simpan Data Baru"):
                    if id_b and jdl:
                        sukses, pesan = tambah_buku(id_b, jdl, pgr, stk) 
                        if sukses:
                            barcode_path = generate_barcode_buku(id_b) 
                            st.success(pesan)
                            st.image(barcode_path, caption=f"Barcode ID {id_b}", width=200)
                            st.markdown(
                                get_image_download_link(barcode_path, f"Barcode_ID_{id_b}.png", "⬇ Download Barcode ID Buku (Statis)"), 
                                unsafe_allow_html=True
                            )
                            time.sleep(2)
                            st.rerun()
                        else:
                            st.error(pesan)
                    else:
                        st.error("ID dan Judul Buku wajib diisi.")

    # --- TAB UPDATE BUKU (Hanya Admin) ---
    if "Update Data" in tab_list:
        with tabs[tab_list.index("Update Data")]:
            st.subheader("Pembaruan Data Buku")
            df_current = muat_data_buku()
            if not df_current.empty:
                id_edit = st.selectbox("Pilih ID Buku yang Ingin Diperbarui", df_current['id_buku'].tolist(), key='update_select')
                buku_terpilih = df_current[df_current['id_buku'] == id_edit].iloc[0]
                
                with st.form("form_update_buku"):
                    jdl_upd = st.text_input("Judul", value=buku_terpilih['judul'])
                    pgr_upd = st.text_input("Pengarang", value=buku_terpilih['pengarang']) 
                    stk_upd = st.number_input("Jumlah Stok", min_value=1, value=int(buku_terpilih['stok']))
                    
                    if st.form_submit_button(" Perbarui Data"):
                        sukses, pesan = update_data_buku(id_edit, jdl_upd, pgr_upd, stk_upd)
                        if sukses:
                            st.success(pesan)
                            st.rerun()
                        else:
                            st.error(pesan)
            else:
                st.info("Tidak ada data untuk diperbarui.")
    
    # --- TAMPILAN DATA MASTER (Untuk Semua Peran) ---
    df_master = muat_data_buku()
    df_master_sorted = df_master.sort_values(by=['pengarang', 'judul']).reset_index(drop=True)

    if "Tabel Master" in tab_list:
        with tabs[tab_list.index("Tabel Master")]:
            st.subheader("Daftar Koleksi Buku")
            st.dataframe(df_master_sorted, use_container_width=True)
            
    # --- HAPUS DATA (Untuk Semua Peran) ---
    if "Hapus Data" in tab_list:
        with tabs[tab_list.index("Hapus Data")]:
            st.subheader("Hapus Data Permanen")
            if not df_master.empty:
                id_hapus = st.selectbox("Pilih ID untuk dihapus", df_master['id_buku'].tolist(), key='delete_key')
                if st.button(" Hapus Permanen"):
                    hapus_buku_permanen(id_hapus)
                    st.warning(f"ID {id_hapus} Dihapus Permanen!")
                    st.rerun()
            else:
                st.info("Tidak ada data untuk dihapus.")


# MENU 3: SCANNER BARCODE (Peminjaman & Pengembalian)
elif menu == "Scanner Barcode ":
    st.title(" Transaksi Peminjaman / Pengembalian Cepat")
    
    mode = st.radio("Pilih Tipe Operasi", ('Peminjaman Satuan', 'Pengembalian Satuan (Scan)', 'Mode Batch (Cepat)'))
    st.markdown("---")
    
    if mode == 'Peminjaman Satuan':
        st.subheader("Peminjaman Buku Satuan")
        
        opsi_buku = get_opsi_peminjaman()
        col_select, col_empty = st.columns([0.7, 0.3])
        pilihan_peminjaman = col_select.selectbox("Pilih Buku yang Ingin Dipinjam:", options=opsi_buku, index=0)
        
        if pilihan_peminjaman != 'Pilih Buku':
            id_buku_pinjam = pilihan_peminjaman.split(' - ')[0]

            if st.button("✅ Proses Peminjaman"):
                hasil = validasi_id_scan(id_buku_pinjam)
                
                if hasil is not None and hasil.iloc[0]['stok'] > 0:
                    kurangi_stok_satu(id_buku_pinjam)
                    trx_id = catat_peminjaman_unik(id_buku_pinjam) 
                    barcode_path = generate_barcode_buku(trx_id) 
                    
                    st.success(f"PINJAM BERHASIL! ID Transaksi: {trx_id}")
                    st.info("Simpan Barcode ini untuk Pengembalian!")
                    st.image(barcode_path, caption=f"Barcode TRX-ID: {trx_id}", width=200)
                    st.markdown(
                        get_image_download_link(barcode_path, f"Barcode_TRX_{trx_id}.png", "⬇ Download Barcode TRX-ID"), 
                        unsafe_allow_html=True
                    )
                else:
                    st.error("Gagal: Stok Habis atau ID Tidak Ditemukan!")

    elif mode == 'Pengembalian Satuan (Scan)':
        st.subheader("Pengembalian Buku Satuan")
        
        col_mode, col_scan = st.columns([0.4, 0.6])
        
        input_mode = col_mode.radio("Pilih Metode Scan:",
            ('Scan Langsung (Webcam)', 'Unggah File Barcode'), index=0)
        
        img_file = None
        
        if input_mode == 'Scan Langsung (Webcam)':
            img_file = col_scan.camera_input("Scanner Webcam")
        elif input_mode == 'Unggah File Barcode':
            img_file = col_scan.file_uploader("Unggah File Barcode TRX (.png/.jpg)", type=['png', 'jpg', 'jpeg'])

        if img_file is not None:
            id_scanned = scan_qr_dari_gambar(img_file) 
            
            if id_scanned:
                st.info(f"Barcode Terbaca: {id_scanned}")
                sukses, id_buku = proses_pengembalian_via_trx(id_scanned)
                
                if sukses:
                    st.success(f"✅ PENGEMBALIAN BERHASIL! Buku {id_buku} bertambah stok 1.")
                else:
                    st.error("❌ Gagal: Transaksi tidak ditemukan, sudah dikembalikan, atau Barcode tidak valid!")
            else:
                st.error("❌ Barcode tidak terbaca dari masukan.")
                
    elif mode == 'Mode Batch (Cepat)':
        st.subheader("Mode Peminjaman/Pengembalian Massal")
        
        batch_mode = st.radio("Pilih Operasi Batch:", ('Peminjaman Batch (ID Buku)', 'Pengembalian Batch (TRX-ID)'))
        st.markdown("---")
        
        if batch_mode == 'Peminjaman Batch (ID Buku)':
            st.info("Masukkan ID Buku yang ingin dipinjam, dipisahkan dengan koma (cth: A001, B005, C002)")
            id_input = st.text_area("Daftar ID Buku", height=100)
            if st.button(" Proses Peminjaman Batch"):
                id_list = [i.strip().upper() for i in id_input.split(',') if i.strip()]
                if id_list:
                    hasil = proses_peminjaman_batch(id_list)
                    if hasil['sukses']:
                        st.success(f"✅ Sukses Meminjam {len(hasil['sukses'])} buku. Total {len(id_list)} item diproses.")
                        
                        st.subheader("Barcode Transaksi (TRX-ID) untuk Pengembalian")
                        with st.expander("Klik untuk Lihat/Download Semua Barcode", expanded=True):
                            for res in hasil['sukses']:
                                trx_id = res['trx_id']
                                id_buku = res['id_buku']
                                
                                barcode_path = generate_barcode_buku(trx_id) 
                                
                                st.markdown(f"**Buku ID: {id_buku}** | **TRX-ID: {trx_id}**")
                                if barcode_path:
                                    st.image(barcode_path, caption=f"Barcode TRX-ID: {trx_id}", width=150)
                                    st.markdown(
                                        get_image_download_link(barcode_path, f"Barcode_TRX_{trx_id}.png", "⬇ Download Barcode TRX-ID"), 
                                        unsafe_allow_html=True
                                    )
                                st.markdown("---") 

                    if hasil['gagal']:
                        st.warning(f"⚠️ Gagal meminjam: {len(hasil['gagal'])} buku.")
                        st.markdown(f"ID Gagal: `{'`, `'.join(hasil['gagal'])}`")
                else:
                    st.warning("Masukkan minimal satu ID Buku.")
                    
        elif batch_mode == 'Pengembalian Batch (TRX-ID)':
            st.info("Masukkan TRX-ID yang ingin dikembalikan, dipisahkan dengan koma.")
            trx_input = st.text_area("Daftar TRX-ID", height=100)
            if st.button(" Proses Pengembalian Batch"):
                trx_list = [t.strip().upper() for t in trx_input.split(',') if t.strip()]
                if trx_list:
                    hasil = proses_pengembalian_batch(trx_list)
                    if hasil['sukses']:
                        st.success(f"✅ Sukses Mengembalikan {len(hasil['sukses'])} buku.")
                    if hasil['gagal']:
                        st.warning(f"⚠️ Gagal mengembalikan: {len(hasil['gagal'])} transaksi (tidak valid/sudah kembali).")
                else:
                    st.warning("Masukkan minimal satu TRX-ID.")


# MENU 4: LOG PEMINJAMAN & LAPORAN
elif menu == "Log Peminjaman & Laporan ":
    st.title(" Riwayat Transaksi & Laporan")
    
    st.subheader("Filter Laporan")
    col_stat, col_date_start, col_date_end = st.columns(3)
    
    df_log_full = muat_data_log()
    
    if df_log_full.empty:
        st.info("Log Transaksi masih kosong. Silakan lakukan peminjaman terlebih dahulu.")
        
    else:
        # --- 2. FILTER BERDASARKAN STATUS ---
        status_filter = col_stat.selectbox("Filter Berdasarkan Status", ['Semua', 'Dipinjam', 'Kembali'])
        df_filtered_status = filter_log_by_status(status_filter) 
        
        # --- 3. FILTER BERDASARKAN TANGGAL ---
        today = datetime.now().date()
        
        try:
            min_date_str = df_log_full['tanggal_pinjam'].min().split(' ')[0]
            default_start = datetime.strptime(min_date_str, '%Y-%m-%d').date()
        except Exception:
            default_start = today.replace(day=1) 
        
        start_date = col_date_start.date_input("Tanggal Mulai", default_start)
        end_date = col_date_end.date_input("Tanggal Akhir", today)
        
        df_display = filter_log_by_date(df_filtered_status, start_date, end_date) 
        
        
        if df_display.empty:
            st.warning("Tidak ada data log yang cocok dengan kriteria filter yang dipilih.")
        else:
            st.dataframe(df_display, use_container_width=True)
            
        # EXPORT KE EXCEL
        if not df_display.empty:
            if st.button("⬇ Export Data Filtered ke Excel"):
                filename = f"Laporan_Log_{start_date}_to_{end_date}"
                excel_path = export_to_excel(df_display, filename)
                
                st.success(f"Laporan tersimpan di: {excel_path}")
                st.markdown(
                    get_binary_file_downloader_html(excel_path, 'Klik di sini untuk Download File Excel'),
                    unsafe_allow_html=True
                )


# MENU 5: PENGATURAN & BACKUP
elif menu == "Pengaturan & Backup ":
    st.title(" Pengaturan Sistem & Data")
    
    if st.session_state['role'] == 'admin':
        st.subheader("Manajemen Backup Data")
        
        col_backup_csv, col_zip = st.columns(2)
        
        if col_backup_csv.button("Trigger Auto-Backup CSV (Master & Log)"):
            timestamp = auto_backup_csv()
            col_backup_csv.success(f"Backup CSV berhasil pada {timestamp}!")

        if col_zip.button("Kompresi Folder Data ke ZIP"):
            zip_filename = compress_data_to_zip()
            col_zip.success(f"Folder dikompresi ke: {zip_filename}")
            
            col_zip.markdown(
                get_binary_file_downloader_html(zip_filename, '⬇ Download File ZIP (Data & QR)'),
                unsafe_allow_html=True
            )
    else:
        st.error("Akses ke Pengaturan & Backup dibatasi hanya untuk Administrator.")

    st.subheader("Informasi Pengguna")
    st.info(f"Anda masuk sebagai: **{st.session_state['username'].upper()} ({st.session_state['role'].upper()})**")
    st.markdown("Aplikasi berjalan 100% secara lokal dan tidak memerlukan internet.")

elif menu == "Tentang":
    st.title("Tentang Aplikasi")
    st.subheader("Sistem Perpustakaan Mini Berbasis Barcode (Streamlit)")

    st.markdown("Aplikasi ini membantu pengelolaan perpustakaan sederhana secara **lokal** (tanpa internet) dengan dukungan **barcode** untuk mempercepat transaksi peminjaman dan pengembalian.")
