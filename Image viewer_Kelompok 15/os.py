import os
import subprocess

# Nama file untuk menyimpan data gambar
FILE_DB = "images.txt"

# =========================
# LOAD & SAVE
# =========================
# Fungsi untuk membaca data gambar dari file TXT
def load_images():
    # Jika file belum ada, program akan membuat file baru
    if not os.path.exists(FILE_DB):
        open(FILE_DB, "w").close()

    # Membaca isi file lalu mengubahnya menjadi list
    with open(FILE_DB, "r") as file:
        return file.read().splitlines()

# Fungsi untuk menyimpan data gambar ke file TXT
def save_images(images):
    with open(FILE_DB, "w") as file:
        for img in images:
            file.write(img + "\n")

# =========================
# CRUD
# =========================
# Fungsi menambah gambar
def tambah_gambar(images):
    path = input("Masukkan path gambar: ")

    # Mengecek apakah file gambar ada
    if os.path.exists(path):
        images.append(path)     # Menambahkan gambar ke list
        save_images(images)     # Menyimpan perubahan ke file
        print("Gambar berhasil ditambahkan!")
    else:
        print("File tidak ditemukan!")

# Fungsi melihat daftar gambar
def lihat_gambar(images):
    if not images:
        print("Belum ada gambar.")
        return

    # Menampilkan semua gambar beserta indexnya
    print("\n=== DAFTAR GAMBAR ===")
    for i, img in enumerate(images):
        print(f"[{i}] {img}")

# Fungsi mengubah data gambar
def update_gambar(images):
    lihat_gambar(images)

    try:
        idx = int(input("Pilih index: "))

        if 0 <= idx < len(images):
            baru = input("Path baru: ")

            # Mengecek apakah file baru ada
            if os.path.exists(baru):
                images[idx] = baru
                save_images(images)
                print("Berhasil diupdate!")
            else:
                print("File tidak ditemukan!")
        else:
            print("Index salah!")

    # Validasi jika input bukan angka
    except ValueError:
        print("Harus angka!")

# Fungsi menghapus gambar
def hapus_gambar(images):
    lihat_gambar(images)

    try:
        idx = int(input("Pilih index: "))

        if 0 <= idx < len(images):       # Mengecek index valid
            deleted = images.pop(idx)    # Menghapus gambar dari list
            save_images(images)
            print(f"{deleted} dihapus.")
        else:
            print("Index salah!")

    except ValueError:
        print("Harus angka!")

# =========================
# OPEN IMAGE
# =========================
# Fungsi untuk membuka gambar langsung dari komputer
def buka_gambar(path):
    try:
        # Untuk Windows
        if os.name == "nt":
            os.startfile(path)

        # Untuk Linux
        elif os.name == "posix":
            subprocess.run(["xdg-open", path])

        else:
            print("OS tidak didukung.")

    except Exception as e:
        print("Gagal membuka gambar:", e)

# =========================
# VIEWER
# =========================
# Fungsi viewer untuk next dan previous gambar
def viewer(images):
    # Jika list kosong
    if not images:
        print("Tidak ada gambar!")
        return

    # Mulai dari gambar pertama
    index = 0

    while True:
        current = images[index]

        print("\n===================")
        print(f"Gambar ke-{index+1}/{len(images)}")
        print(current)
        print("===================")

        # Membuka gambar
        buka_gambar(current)

        # Input pilihan user
        pilih = input("[N] Next | [P] Prev | [Q] Quit : ").lower()

        # Next gambar
        if pilih == "n":
            index = (index + 1) % len(images)

        # Previous gambar
        elif pilih == "p":
            index = (index - 1) % len(images)

        # Keluar viewer
        elif pilih == "q":
            break

        else:
            print("Input salah!")

# =========================
# MAIN
# =========================
def main():
    # Load data gambar dari file
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

        # Menjalankan menu sesuai pilihan user
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

# Menjalankan program utama
main()