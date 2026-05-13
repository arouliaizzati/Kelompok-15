import os
import subprocess

# Nama file untuk menyimpan data gambar
FILE_DB = "images.txt"

# =========================
# LOAD & SAVE
# =========================
# Fungsi untuk membaca data gambar dari file TXT
def load_images():
    if not os.path.exists(FILE_DB):
        open(FILE_DB, "w").close()

    with open(FILE_DB, "r") as file:
        return file.read().splitlines()

def save_images(images):
    with open(FILE_DB, "w") as file:
        for img in images:
            file.write(img + "\n")

# =========================
# CRUD
# =========================
def tambah_gambar(images):
    path = input("Masukkan path gambar: ")

    if os.path.exists(path):
        images.append(path)
        save_images(images)
        print("Gambar berhasil ditambahkan!")
    else:
        print("File tidak ditemukan!")

def lihat_gambar(images):
    if not images:
        print("Belum ada gambar.")
        return

    print("\n=== DAFTAR GAMBAR ===")
    for i, img in enumerate(images):
        print(f"[{i}] {img}")

def update_gambar(images):
    lihat_gambar(images)

    try:
        idx = int(input("Pilih index: "))

        if 0 <= idx < len(images):
            baru = input("Path baru: ")

            if os.path.exists(baru):
                images[idx] = baru
                save_images(images)
                print("Berhasil diupdate!")
            else:
                print("File tidak ditemukan!")
        else:
            print("Index salah!")

    except ValueError:
        print("Harus angka!")

def hapus_gambar(images):
    lihat_gambar(images)

    try:
        idx = int(input("Pilih index: "))

        if 0 <= idx < len(images):
            deleted = images.pop(idx)
            save_images(images)
            print(f"{deleted} dihapus.")
        else:
            print("Index salah!")

    except ValueError:
        print("Harus angka!")

# =========================
# OPEN IMAGE
# =========================
def buka_gambar(path):
    try:
        if os.name == "nt":
            os.startfile(path)

        elif os.name == "posix":
            subprocess.run(["xdg-open", path])

        else:
            print("OS tidak didukung.")

    except Exception as e:
        print("Gagal membuka gambar:", e)

# =========================
# VIEWER
# =========================
def viewer(images):
    if not images:
        print("Tidak ada gambar!")
        return

    index = 0

    while True:
        current = images[index]

        print("\n===================")
        print(f"Gambar ke-{index+1}/{len(images)}")
        print(current)
        print("===================")

        buka_gambar(current)

        pilih = input("[N] Next | [P] Prev | [Q] Quit : ").lower()

        if pilih == "n":
            index = (index + 1) % len(images)

        elif pilih == "p":
            index = (index - 1) % len(images)

        elif pilih == "q":
            break

        else:
            print("Input salah!")

# =========================
# MAIN
# =========================
def main():
    images = load_images()

    while True:
        print("\n====== IMAGE REVIEWER ======")
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

main()