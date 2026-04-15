def load_images():
    try:
        with open("images.txt", "r") as file:
            images = file.read().splitlines()
            return images
    except FileNotFoundError:
        print("File tidak ditemukan, membuat file baru...")
        return []

def save_images(images):
    with open("images.txt", "w") as file:
        for img in images:
            file.write(img + "\n")

# CRUD
def tambah_gambar(images):
    nama = input("Masukkan nama file gambar: ")
    images.append(nama)
    save_images(images)

def lihat_gambar(images):
    print("\nDaftar Gambar:")
    for i, img in enumerate(images):
        print(f"{i}. {img}")

def update_gambar(images):
    lihat_gambar(images)
    try:
        idx = int(input("Pilih index yang mau diubah: "))
        if 0 <= idx < len(images):
            nama_baru = input("Nama baru: ")
            images[idx] = nama_baru
            save_images(images)
        else:
            print("Index tidak valid!")
    except ValueError:
        print("Input harus angka!")

def hapus_gambar(images):
    lihat_gambar(images)
    try:
        idx = int(input("Pilih index yang mau dihapus: "))
        if 0 <= idx < len(images):
            images.pop(idx)
            save_images(images)
        else:
            print("Index tidak valid!")
    except ValueError:
        print("Input harus angka!")

# Viewer
def viewer(images):
    if not images:
        print("Tidak ada gambar!")
        return
    
    index = 0
    while True:
        print(f"\nMenampilkan: {images[index]}")
        pilihan = input("[n] Next | [p] Prev | [q] Quit: ")

        if pilihan == "n":
            index = (index + 1) % len(images)
        elif pilihan == "p":
            index = (index - 1) % len(images)
        elif pilihan == "q":
            break
        else:
            print("Input salah!")

# MAIN MENU
def main():
    images = load_images()

    while True:
        print("\n=== MENU ===")
        print("1. Lihat Data")
        print("2. Tambah")
        print("3. Update")
        print("4. Hapus")
        print("5. Viewer")
        print("6. Keluar")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            lihat_gambar(images)
        elif pilihan == "2":
            tambah_gambar(images)
        elif pilihan == "3":
            update_gambar(images)
        elif pilihan == "4":
            hapus_gambar(images)
        elif pilihan == "5":
            viewer(images)
        elif pilihan == "6":
            print("Keluar...")
            break
        else:
            print("Pilihan tidak valid!")

main()