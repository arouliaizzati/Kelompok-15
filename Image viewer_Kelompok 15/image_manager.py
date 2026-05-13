import os
import subprocess

# Nama file database
FILE_DB = "images.txt"

# =========================
# LOAD & SAVE
# =========================
def load_images():
    if not os.path.exists(FILE_DB):
        open(FILE_DB, "w").close()

    data = []
    try:
        with open(FILE_DB, "r") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                
                # Logika fleksibel: Bisa baca format Nama|Path atau format lama (hanya nama)
                if "|" in line:
                    nama, path = line.split("|")
                    data.append({"nama": nama, "path": path})
                else:
                    # Jika data lama hanya berisi nama file, gunakan itu untuk keduanya
                    data.append({"nama": line, "path": line})
    except Exception as e:
        print("Gagal memuat data:", e)
        
    return data

def save_images(images):
    try:
        with open(FILE_DB, "w") as file:
            for img in images:
                file.write(f"{img['nama']}|{img['path']}\n")
    except Exception as e:
        print("Gagal menyimpan data:", e)

# =========================
# CRUD
# =========================
def tambah_gambar(images):
    print("\n--- Tambah Gambar Baru ---")
    nama = input("Masukkan Nama/Label Gambar: ")
    path = input("Masukkan Path/Nama File (misal: langit.jpg): ")

    if os.path.exists(path):
        images.append({"nama": nama, "path": path})
        save_images(images)
        print("Data berhasil disimpan.")
    else:
        print("File fisik tidak ditemukan. Pastikan file ada di folder yang sama.")

def lihat_gambar(images):
    if not images:
        print("\n[ Galeri masih kosong ]")
        return

    # Tampilan Tabel Manusiawi
    print("\n" + "="*70)
    print(f"{'ID':<4} | {'NAMA GAMBAR':<30} | {'PATH FILE':<30}")
    print("-" * 70)
    for i, img in enumerate(images):
        print(f"{i:<4} | {img['nama']:<30} | {img['path']:<30}")
    print("="*70)

def update_gambar(images):
    lihat_gambar(images)
    try:
        idx = int(input("\nPilih ID yang mau diubah: "))
        if 0 <= idx < len(images):
            print(f"Mengubah data: {images[idx]['nama']}")
            nama_baru = input("Nama baru: ")
            path_baru = input("Path baru: ")

            if os.path.exists(path_baru):
                images[idx] = {"nama": nama_baru, "path": path_baru}
                save_images(images)
                print("Data berhasil diperbarui.")
            else:
                print("File tidak ditemukan.")
        else:
            print("ID tidak valid.")
    except ValueError:
        print("Input harus berupa angka.")

def hapus_gambar(images):
    lihat_gambar(images)
    try:
        idx = int(input("\nPilih ID yang mau dihapus: "))
        if 0 <= idx < len(images):
            deleted = images.pop(idx)
            save_images(images)
            print(f"Data '{deleted['nama']}' telah dihapus.")
        else:
            print("ID tidak ditemukan.")
    except ValueError:
        print("Input harus berupa angka.")

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
        print(f"Gagal membuka file '{path}': {e}")

def viewer(images):
    if not images:
        print("Galeri kosong.")
        return

    index = 0
    while True:
        current = images[index]
        print(f"\n>>> Menampilkan: {current['nama']} ({index+1}/{len(images)})")
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
        print("\n--- SISTEM MANAJEMEN GAMBAR ---")
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
        elif pilih == "6": 
            print("Program selesai.")
            break
        else: 
            print("Pilihan tidak valid.")

if __name__ == "__main__":
    main()