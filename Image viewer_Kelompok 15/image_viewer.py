class ImageViewer:
    def __init__(self):
        self.photos = []          # list dinamis (tidak boros memori)
        self.current_index = 0    # penunjuk foto aktif

    def add_photo(self, filename):
        self.photos.append(filename)

    def show_current(self):
        if not self.photos:
            print("Galeri kosong.")
        else:
            print(f"Foto saat ini: {self.photos[self.current_index]}")

    def next_photo(self):
        if not self.photos:
            print("Galeri kosong.")
        else:
            self.current_index = (self.current_index + 1) % len(self.photos)

    def prev_photo(self):
        if not self.photos:
            print("Galeri kosong.")
        else:
            self.current_index = (self.current_index - 1) % len(self.photos)


# ===== Program Utama =====
viewer = ImageViewer()

# Input awal foto
n = int(input("Masukkan jumlah foto: "))
for i in range(n):
    nama = input(f"Nama file foto ke-{i+1}: ")
    viewer.add_photo(nama)

while True:
    print("\n=== MENU ===")
    print("1. Tampilkan Foto")
    print("2. Next")
    print("3. Prev")
    print("4. Exit")

    pilihan = input("Pilih menu: ")

    if pilihan == "1":
        viewer.show_current()
    elif pilihan == "2":
        viewer.next_photo()
        viewer.show_current()
    elif pilihan == "3":
        viewer.prev_photo()
        viewer.show_current()
    elif pilihan == "4":
        print("Program selesai.")
        break
    else:
        print("Pilihan tidak valid.")
