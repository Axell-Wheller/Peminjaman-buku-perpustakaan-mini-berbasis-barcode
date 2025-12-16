import pandas as pd
import os
import barcode
from barcode.writer import ImageWriter
from pyzbar.pyzbar import decode
from PIL import Image
import numpy as np
import uuid
from datetime import datetime
import shutil 
from zipfile import ZipFile 

# --- A. FUNGSI MANAJEMEN DATA DASAR (Fungsi 1-5) ---

# 1. Muat data buku master
def muat_data_buku(path='data/master.csv'):
    if not os.path.exists(path):
        df = pd.DataFrame(columns=['id_buku', 'judul', 'pengarang', 'stok'])
        df.to_csv(path, index=False)
    return pd.read_csv(path)

# 2. Muat log peminjaman
def muat_data_log(path='data/log.csv'):
    if not os.path.exists(path):
        df = pd.DataFrame(columns=['id_transaksi', 'id_buku', 'tanggal_pinjam', 'status'])
        df.to_csv(path, index=False)
    return pd.read_csv(path)

# 3. Simpan permanen ke CSV
def simpan_ke_csv(df, target):
    df.to_csv(f'data/{target}.csv', index=False)

# 4. Tambah Buku (CRUD Create)
def tambah_buku(id_b, jdl, pgr, stk):
    df = muat_data_buku()
    if id_b in df['id_buku'].tolist():
        return False, f"Gagal: ID Buku '{id_b}' sudah ada di database." 
    
    baru = pd.DataFrame([[id_b, jdl, pgr, stk]], columns=df.columns)
    df = pd.concat([df, baru], ignore_index=True)
    df = df.sort_values(by=['id_buku']).reset_index(drop=True)
    simpan_ke_csv(df, 'master')
    return True, f"Buku '{jdl}' berhasil disimpan."

# 5. Hapus Buku (CRUD Delete)
def hapus_buku_permanen(id_b):
    df = muat_data_buku()
    df = df[df['id_buku'] != str(id_b)]
    simpan_ke_csv(df, 'master')
    
# --- B. FUNGSI BARCODE & TRANSAKSI (Fungsi 6-11) ---

# 6. Generate Barcode
def generate_barcode_buku(id_code):
    try:
        Code128 = barcode.get_barcode_class('code128')
        instance = Code128(str(id_code), writer=ImageWriter())
        
        file_path = f"qr/{id_code}.png" 
        
        instance.write(open(file_path, 'wb'), 
                       options={'write_text': True, 
                                'module_height': 15.0, 
                                'font_size': 12, 
                                'text_distance': 5,
                                'quiet_zone': 4.0,
                                'dpi': 300,
                                'module_width': 0.2})
        return file_path
    except Exception as e:
        print(f"Error generating barcode: {e}")
        return None 

# 7. Validasi ID saat scan
def validasi_id_scan(id_input):
    df = muat_data_buku()
    match = df[df['id_buku'] == str(id_input)]
    return match if not match.empty else None

# 8. Kurangi stok tepat 1
def kurangi_stok_satu(id_b):
    df = muat_data_buku()
    idx = df.index[df['id_buku'] == str(id_b)].tolist()
    if idx and df.at[idx[0], 'stok'] > 0:
        df.at[idx[0], 'stok'] -= 1
        simpan_ke_csv(df, 'master')
        return True
    return False

# 9. Catat Peminjaman
def catat_peminjaman_unik(id_b):
    df_log = muat_data_log()
    trx_id = str(uuid.uuid4()).split('-')[0].upper() 
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    baru = pd.DataFrame([[trx_id, id_b, waktu, 'Dipinjam']], columns=df_log.columns)
    df_log = pd.concat([df_log, baru], ignore_index=True)
    simpan_ke_csv(df_log, 'log')
    return trx_id

# 10. Proses Pengembalian via TRX-ID
def proses_pengembalian_via_trx(trx_id):
    df_log = muat_data_log()
    transaksi = df_log[(df_log['id_transaksi'] == trx_id) & (df_log['status'] == 'Dipinjam')]
    
    if not transaksi.empty:
        id_buku = transaksi.iloc[0]['id_buku']
        
        df = muat_data_buku()
        idx = df.index[df['id_buku'] == str(id_buku)].tolist()
        if idx:
            df.at[idx[0], 'stok'] += 1
            simpan_ke_csv(df, 'master')
        
        df_log.loc[df_log['id_transaksi'] == trx_id, 'status'] = 'Kembali'
        simpan_ke_csv(df_log, 'log')
        
        return True, id_buku
    return False, None

# 11. Dekode Barcode dari gambar kamera/file
def scan_qr_dari_gambar(img_file):
    img = Image.open(img_file)
    img_np = np.array(img)
    decoded = decode(img_np) 
    if decoded:
        return decoded[0].data.decode("utf-8")
    return None

# --- C. FUNGSI LAPORAN & FILTERING (Fungsi 12-16) ---

# 12. Dashboard Statistik
def ringkasan_data_dasbor():
    buku = muat_data_buku()
    log = muat_data_log()
    dipinjam = log[log['status'] == 'Dipinjam'].shape[0]
    return len(buku), len(log), dipinjam

# 13. Get Opsi Selectbox
def get_opsi_peminjaman():
    df = muat_data_buku()
    df_tersedia = df[df['stok'] > 0]
    opsi = (df_tersedia['id_buku'] + ' - ' + df_tersedia['judul']).tolist()
    return ['Pilih Buku'] + opsi 

# 14. Filter Log Berdasarkan Tanggal (FIXED LOGIC)
def filter_log_by_date(df_input, start_date, end_date):
    
    df = df_input.copy()
    df['tanggal_pinjam_dt'] = pd.to_datetime(df['tanggal_pinjam']).dt.date
    
    if isinstance(start_date, datetime):
        start_date = start_date.date()
    if isinstance(end_date, datetime):
        end_date = end_date.date()
        
    filtered_df = df[(df['tanggal_pinjam_dt'] >= start_date) & (df['tanggal_pinjam_dt'] <= end_date)]
    
    filtered_df = filtered_df.drop(columns=['tanggal_pinjam_dt'])
    
    return filtered_df

# 15. Filter Log Berdasarkan Status
def filter_log_by_status(status):
    df = muat_data_log()
    if status == 'Semua':
        return df
    return df[df['status'] == status]

# 16. Export DataFrame ke Excel
def export_to_excel(df, filename):
    path = f"data/laporan/{filename}.xlsx"
    df.to_excel(path, index=False, engine='xlsxwriter')
    return path

# --- D. FUNGSI ADVANCED (Fungsi 17-23) ---

# 17. Validasi Login Sederhana (Mengembalikan Peran)
def otentikasi_user(username, password):
    akun = {
        'admin': {'password': '12345', 'role': 'admin'},
        'kasir': {'password': 'abcde', 'role': 'kasir'}
    }
    if username in akun and akun[username]['password'] == password:
        return True, akun[username]['role']
    return False, None

# 18. Auto Backup File CSV
def auto_backup_csv():
    backup_dir = 'data/backup'
    os.makedirs(backup_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    for filename in ['master.csv', 'log.csv']:
        src = os.path.join('data', filename)
        dst = os.path.join(backup_dir, f'{filename.replace(".csv", "")}_backup_{timestamp}.csv')
        if os.path.exists(src):
            shutil.copyfile(src, dst)
        
    return timestamp

# 19. Kompresi Folder Data ke ZIP
def compress_data_to_zip():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"backup_data_{timestamp}.zip"
    
    with ZipFile(zip_filename, 'w') as zipf:
        for folder in ['data', 'qr']:
            if os.path.isdir(folder):
                for root, _, files in os.walk(folder):
                    for file in files:
                        file_path = os.path.join(root, file)
                        zipf.write(file_path, arcname=os.path.join(folder, file))
    return zip_filename

# 20. Proses Peminjaman Batch
def proses_peminjaman_batch(id_list):
    hasil = {'sukses': [], 'gagal': []}
    for id_buku in id_list:
        if kurangi_stok_satu(id_buku):
            trx_id = catat_peminjaman_unik(id_buku)
            hasil['sukses'].append({'id_buku': id_buku, 'trx_id': trx_id})
        else:
            hasil['gagal'].append(id_buku)
    return hasil

# 21. Proses Pengembalian Batch
def proses_pengembalian_batch(trx_list):
    hasil = {'sukses': [], 'gagal': []}
    for trx_id in trx_list:
        sukses, id_buku = proses_pengembalian_via_trx(trx_id)
        if sukses:
            hasil['sukses'].append(id_buku)
        else:
            hasil['gagal'].append(trx_id)
    return hasil

# 22. Fungsi Update Buku
def update_data_buku(id_b, jdl, pgr, stk):
    df = muat_data_buku()
    idx = df.index[df['id_buku'] == str(id_b)].tolist()
    
    if idx:
        i = idx[0]
        df.at[i, 'judul'] = jdl
        df.at[i, 'pengarang'] = pgr
        df.at[i, 'stok'] = int(stk)
        simpan_ke_csv(df, 'master')
        return True, f"Data buku {id_b} berhasil diperbarui."
    return False, f"ID Buku {id_b} tidak ditemukan."

# 23. Fungsi Data Log Terbaru
def get_log_terbaru(n=5):
    df = muat_data_log()
    return df.tail(n).sort_index(ascending=False)