import os
import subprocess

# Nama file database
FILE_DB = "images.txt"

# =========================
# LOAD & SAVE (LOGIKA BARU)
# =========================
def load_images():
    if not os.path.exists(FILE_DB):
        open(FILE_DB, "w").close()v

    data = []
    with open(FILE_DB, "r") as file:
        for line in file:
            # Kita pakai pemisah "|" untuk membagi nama dan path
            if "|" in line:
                nama, path = line.strip().split("|")
                data.append({"nama": nama, "path": path})
    return data

def save_images(images):
    with open(FILE_DB, "w") as file:
        for img in images:
            # Simpan dengan format: Nama|Path
            file.write(f"{img['nama']}|{img['path']}\n")

# =========================
# CRUD (DENGAN TAMPILAN TABEL)
# =========================
def tambah_gambar(images):
    print("\n--- Tambah Gambar Baru ---")
    nama = input("Masukkan Nama/Label Gambar: ")
    path = input("Masukkan Path/Nama File (misal: langit.jpg): ")

    if os.path.exists(path):
        images.append({"nama": nama, "path": path})
        save_images(images)
        print("Berhasil disimpan ke tabel!")
    else:
        print("File tidak ditemukan! Pastikan file ada di folder yang sama.")

def lihat_gambar(images):
    if not images:
        print("\n[ Galeri masih kosong ]")
        return

    # TAMPILAN TABEL
    print("\n" + "="*60)
    print(f"{'ID':<4} | {'NAMA GAMBAR':<25} | {'PATH FILE':<25}")
    print("-" * 60)
    for i, img in enumerate(images):
        print(f"{i:<4} | {img['nama']:<25} | {img['path']:<25}")
    print("="*60)

def update_gambar(images):
    lihat_gambar(images)
    try:
        idx = int(input("\nPilih ID yang mau diubah: "))
        if 0 <= idx < len(images):
            print(f"Mengubah: {images[idx]['nama']}")
            nama_baru = input("Nama baru: ")
            path_baru = input("Path baru: ")

            if os.path.exists(path_baru):
                images[idx] = {"nama": nama_baru, "path": path_baru}
                save_images(images)
                print("Data diperbarui!")
            else:
                print("File tidak ditemukan!")
        else:
            print("ID salah!")
    except ValueError:
        print("Input harus angka!")

def hapus_gambar(images):
    lihat_gambar(images)
    try:
        idx = int(input("\nPilih ID yang mau dihapus: "))
        if 0 <= idx < len(images):
            deleted = images.pop(idx)
            save_images(images)
            print(f"🗑️ '{deleted['nama']}' dihapus.")
        else:
            print("ID tidak ditemukan!")
    except ValueError:
        print("Input harus angka!")

# =========================
# OPEN & VIEWER
# =========================
def buka_gambar(path):
    try:
        if os.name == "nt": # Windows
            os.startfile(path)
        elif os.name == "posix": # Linux/Mac
            subprocess.run(["xdg-open", path])
    except Exception as e:
        print("Gagal membuka file:", e)

def viewer(images):
    if not images:
        print("Galeri kosong!")
        return

    index = 0
    while True:
        current = images[index]
        print(f"\n>>> Menampilkan: {current['nama']} ({index+1}/{len(images)})")
        
        # Buka gambarnya beneran
        buka_gambar(current['path'])

        pilih = input("[N] Next | [P] Prev | [Q] Keluar Viewer: ").lower()
        if pilih == "n":
            index = (index + 1) % len(images)
        elif pilih == "p":
            index = (index - 1) % len(images)
        elif pilih == "q":
            break

# =========================
# MAIN MENU
# =========================
def main():
    images = load_images()
    while True:
        print("\nIMAGE REVIEWER")
        print("1. Lihat Tabel Gambar")
        print("2. Tambah Data")
        print("3. Update Data")
        print("4. Hapus Data")
        print("5. Jalankan Viewer")
        print("6. Keluar")

        pilih = input("Pilih menu: ")
        if pilih == "1": lihat_gambar(images)
        elif pilih == "2": tambah_gambar(images)
        elif pilih == "3": update_gambar(images)
        elif pilih == "4": hapus_gambar(images)
        elif pilih == "5": viewer(images)
        elif pilih == "6": break
        else: print("Pilihan salah!")

if __name__ == "__main__":
    main()