import os
import subprocess

# Nama file database untuk menyimpan daftar gambar
FILE_DB = "images.txt"

# Path default tempat penyimpanan gambar
DEFAULT_PATH = "C:\\image"

# =========================
# LOAD & SAVE DATA
# =========================
def load_images():
    # Jika file database belum ada, buat file kosong
    if not os.path.exists(FILE_DB):
        open(FILE_DB, "w").close()

    images = []
    # Membaca isi file dan memisahkan data berdasarkan tanda '|'
    with open(FILE_DB, "r") as file:
        for line in file:
            if line.strip():
                id, nama, path = line.strip().split("|")
                # Simpan data dalam bentuk dictionary agar lebih terstruktur
                images.append({"id": int(id), "nama": nama, "path": path})
    return images

def save_images(images):
    # Menyimpan semua data gambar ke file database
    with open(FILE_DB, "w") as file:
        for img in images:
            file.write(f"{img['id']}|{img['nama']}|{img['path']}\n")

# =========================
# CRUD DATA
# =========================
def lihat_gambar(images):
    # Menampilkan data gambar dalam bentuk tabel dengan garis kolom
    if not images:
        print("Belum ada gambar.")
        return

    print("\n======================= DAFTAR GAMBAR =======================")

    # Header tabel
    print("+----+----------------------+--------------------------------+")
    print("| ID | Nama                 | Path                           |")
    print("+----+----------------------+--------------------------------+")

    # Isi tabel
    for img in images:
        print(f"| {str(img['id']).ljust(2)} | {img['nama'].ljust(20)} | {img['path'].ljust(30)} |")

    # Footer tabel
    print("+----+----------------------+--------------------------------+")


def tambah_gambar(images):
    # Input hanya nama gambar, path otomatis diarahkan ke folder default
    nama = input("Masukkan nama gambar: ")
    path = os.path.join(DEFAULT_PATH, nama)
    new_id = len(images) + 1  # ID otomatis bertambah sesuai jumlah data
    images.append({"id": new_id, "nama": nama, "path": path})
    save_images(images)
    print("Gambar berhasil ditambahkan!")

def update_gambar(images):
    # Update data berdasarkan ID
    lihat_gambar(images)
    try:
        id_update = int(input("Masukkan ID gambar yang ingin diupdate: "))
        for img in images:
            if img['id'] == id_update:
                nama_baru = input("Masukkan nama gambar baru: ")
                img['nama'] = nama_baru
                img['path'] = os.path.join(DEFAULT_PATH, nama_baru)
                save_images(images)
                print("Berhasil diupdate!")
                return
        print("ID tidak ditemukan!")
    except ValueError:
        print("Harus angka!")

def hapus_gambar(images):
    # Hapus data berdasarkan ID
    lihat_gambar(images)
    try:
        id_hapus = int(input("Masukkan ID gambar yang ingin dihapus: "))
        for img in images:
            if img['id'] == id_hapus:
                images.remove(img)
                save_images(images)
                print("Berhasil dihapus!")
                return
        print("ID tidak ditemukan!")
    except ValueError:
        print("Harus angka!")

# =========================
# MEMBUKA GAMBAR
# =========================
def buka_gambar(path):
    # Membuka file gambar sesuai sistem operasi
    try:
        if os.name == "nt":  # Windows
            os.startfile(path)
        elif os.name == "posix":  # Linux
            subprocess.run(["xdg-open", path])
        else:
            print("OS tidak didukung.")
    except Exception as e:
        print("Gagal membuka gambar:", e)

# =========================
# VIEWER
# =========================
def viewer(images):
    # Fungsi untuk melihat gambar satu per satu (Next/Prev)
    if not images:
        print("Tidak ada gambar!")
        return
    index = 0
    while True:
        current = images[index]
        print("\n===================")
        print(f"Gambar ke-{index+1}/{len(images)}")
        print(f"Nama: {current['nama']}")
        print(f"Path: {current['path']}")
        print("===================")
        buka_gambar(current['path'])
        pilih = input("[N] Next | [P] Prev | [Q] Quit : ").lower()
        if pilih == "n":
            index = (index + 1) % len(images)  # Geser ke kanan
        elif pilih == "p":
            index = (index - 1) % len(images)  # Geser ke kiri
        elif pilih == "q":
            break
        else:
            print("Input salah!")

# =========================
# MENU UTAMA
# =========================
def main():
    # Load data dari file database
    images = load_images()
    while True:
        print("\n====== IMAGE VIEWER ======")
        print("1. Lihat Data")
        print("2. Tambah Gambar")
        print("3. Update Gambar")
        print("4. Hapus Gambar")
        print("5. Viewer")
        print("6. Keluar")
        pilih = input("Pilih menu: ")
        if pilih == "1":
            lihat_gambar(images)
        elif pilih == "2":
            tambah_gambar(images)
        elif pilih == "3":
            update_gambar(images)
        elif pilih == "4":
            hapus_gambar(images)
        elif pilih == "5":
            viewer(images)
        elif pilih == "6":
            print("Program selesai.")
            break
        else:
            print("Menu tidak valid!")

# Jalankan program utama
main()
