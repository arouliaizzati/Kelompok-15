# Import library os untuk akses file/folder dan operasi sistem
import os

# Import subprocess untuk menjalankan program eksternal
import subprocess


# ============================================================
# KONFIGURASI
# ============================================================

# Nama file database penyimpanan data gambar
FILE_DB = "images.txt"

# Folder default tempat gambar disimpan
DEFAULT_PATH = "C:\\image"


# ============================================================
# CLASS NODE
# Menyimpan data satu gambar
# ============================================================

class Node:

    # Constructor class Node
    def __init__(self, id, nama, path):

        # Menyimpan ID gambar
        self.id = id

        # Menyimpan nama file gambar
        self.nama = nama

        # Menyimpan lokasi/path gambar
        self.path = path

        # Pointer ke node berikutnya
        self.next = None

        # Pointer ke node sebelumnya
        self.prev = None


# ============================================================
# CLASS DOUBLY LINKED LIST
# Mengelola semua node gambar
# ============================================================

class DoublyLinkedList:

    # Constructor class DoublyLinkedList
    def __init__(self):

        # Node pertama
        self.head = None

        # Node terakhir
        self.tail = None

        # ID otomatis bertambah
        self._id_seq = 1


    # ========================================================
    # APPEND
    # Tambah node baru ke akhir linked list
    # ========================================================

    def append(self, nama, path, id=None):

        # Jika ada ID gunakan ID tersebut, kalau tidak pakai auto increment
        node_id = id if id is not None else self._id_seq

        # Jika ID lebih besar dari ID sekarang
        if node_id >= self._id_seq:

            # Update auto increment
            self._id_seq = node_id + 1

        # Membuat node baru
        new_node = Node(node_id, nama, path)

        # Jika linked list kosong
        if self.head is None:

            # Node baru jadi head
            self.head = new_node

            # Node baru juga jadi tail
            self.tail = new_node

        else:

            # Pointer prev node baru menunjuk tail lama
            new_node.prev = self.tail

            # Pointer next tail lama menunjuk node baru
            self.tail.next = new_node

            # Tail dipindah ke node baru
            self.tail = new_node

        # Mengembalikan node baru
        return new_node


    # ========================================================
    # FIND BY ID
    # Cari node berdasarkan ID
    # ========================================================

    def find_by_id(self, target_id):

        # Mulai traversal dari head
        cur = self.head

        # Selama node masih ada
        while cur:

            # Jika ID cocok
            if cur.id == target_id:

                # Return node tersebut
                return cur

            # Pindah ke node berikutnya
            cur = cur.next

        # Jika tidak ditemukan return None
        return None


    # ========================================================
    # UPDATE BY ID
    # Mengubah data node
    # ========================================================

    def update_by_id(self, target_id, nama_baru, path_baru):

        # Cari node berdasarkan ID
        node = self.find_by_id(target_id)

        # Jika node ditemukan
        if node:

            # Update nama baru
            node.nama = nama_baru

            # Update path baru
            node.path = path_baru

            # Return berhasil
            return True

        # Jika gagal return False
        return False


    # ========================================================
    # DELETE BY ID
    # Menghapus node dari linked list
    # ========================================================

    def delete_by_id(self, target_id):

        # Cari node berdasarkan ID
        node = self.find_by_id(target_id)

        # Jika node tidak ditemukan
        if not node:

            # Return gagal
            return False

        # Jika ada node sebelumnya
        if node.prev:

            # Sambungkan prev ke next
            node.prev.next = node.next

        else:

            # Jika node adalah head
            self.head = node.next

        # Jika ada node setelahnya
        if node.next:

            # Sambungkan next ke prev
            node.next.prev = node.prev

        else:

            # Jika node adalah tail
            self.tail = node.prev

        # Putus pointer prev
        node.prev = None

        # Putus pointer next
        node.next = None

        # Return berhasil
        return True


    # ========================================================
    # TO LIST
    # Mengubah linked list jadi list biasa
    # ========================================================

    def to_list(self):

        # List kosong
        result = []

        # Mulai traversal dari head
        cur = self.head

        # Selama node masih ada
        while cur:

            # Tambahkan node ke list
            result.append(cur)

            # Pindah ke node berikutnya
            cur = cur.next

        # Return list hasil
        return result


    # ========================================================
    # SEARCH BY ID
    # Mencari node berdasarkan ID
    # ========================================================

    def search_by_id(self, target_id):

        # Cari node
        node = self.find_by_id(target_id)

        # Jika ada return list berisi node
        return [node] if node else []


    # ========================================================
    # SEARCH BY NAMA
    # Cari gambar berdasarkan nama file
    # ========================================================

    def search_by_nama(self, keyword):

        # Ubah keyword jadi lowercase
        keyword = keyword.lower()

        # List hasil pencarian
        hasil = []

        # Mulai traversal dari head
        cur = self.head

        # Selama node masih ada
        while cur:

            # Ambil nama file tanpa ekstensi
            nama_tanpa_ext = os.path.splitext(cur.nama)[0].lower()

            # Jika keyword ditemukan
            if keyword in nama_tanpa_ext or keyword in cur.nama.lower():

                # Tambahkan node ke hasil
                hasil.append(cur)

            # Pindah ke node berikutnya
            cur = cur.next

        # Return hasil pencarian
        return hasil


# ============================================================
# LOAD IMAGES
# Membaca data dari file txt
# ============================================================

def load_images(dll):

    # Jika file database belum ada
    if not os.path.exists(FILE_DB):

        # Buat file kosong
        open(FILE_DB, "w").close()

    # Buka file database mode read
    with open(FILE_DB, "r") as f:

        # Membaca setiap baris
        for line in f:

            # Jika baris tidak kosong
            if line.strip():

                # Pisahkan data berdasarkan |
                parts = line.strip().split("|")

                # Jika jumlah data ada 3
                if len(parts) == 3:

                    # Ambil isi data
                    id_, nama, path = parts

                    # Tambahkan ke linked list
                    dll.append(nama, path, id=int(id_))


# ============================================================
# SAVE IMAGES
# Menyimpan data ke file txt
# ============================================================

def save_images(dll):

    # Buka file mode write
    with open(FILE_DB, "w") as f:

        # Loop semua node
        for node in dll.to_list():

            # Tulis data ke file
            f.write(f"{node.id}|{node.nama}|{node.path}\n")


# ============================================================
# CETAK TABEL
# Menampilkan data dalam bentuk tabel
# ============================================================

def cetak_tabel(nodes):

    # Jika data kosong
    if not nodes:

        # Tampilkan pesan
        print("  Data tidak ditemukan.")

        # Keluar function
        return

    # Cari panjang ID terbesar
    col_id = max(len(str(n.id)) for n in nodes)

    # Minimal lebar 2
    col_id = max(col_id, 2)

    # Cari panjang nama terbesar
    col_nama = max(len(n.nama) for n in nodes)

    # Minimal selebar teks header
    col_nama = max(col_nama, len("Nama Gambar"))

    # Cari panjang path terbesar
    col_path = max(len(n.path) for n in nodes)

    # Minimal selebar header
    col_path = max(col_path, len("Path Gambar"))

    # Membuat garis tabel
    sep = f"+{'-'*(col_id+2)}+{'-'*(col_nama+2)}+{'-'*(col_path+2)}+"

    # Membuat header tabel
    header = (
        f"| {'ID'.center(col_id)} "
        f"| {'Nama Gambar'.ljust(col_nama)} "
        f"| {'Path Gambar'.ljust(col_path)} |"
    )

    # Print garis atas
    print(sep)

    # Print header
    print(header)

    # Print garis tengah
    print(sep)

    # Loop semua node
    for n in nodes:

        # Print isi tabel
        print(
            f"| {str(n.id).center(col_id)} "
            f"| {n.nama.ljust(col_nama)} "
            f"| {n.path.ljust(col_path)} |"
        )

    # Print garis bawah
    print(sep)


# ============================================================
# BUKA GAMBAR
# Membuka file gambar menggunakan program default OS
# ============================================================

def buka_gambar(path):

    # Jika file ada
    if os.path.exists(path):

        try:

            # Untuk Windows gunakan os.startfile
            if os.name == "nt":
                os.startfile(path)

            # Untuk macOS gunakan open
            elif os.uname().sysname == "Darwin":
                subprocess.Popen(["open", path])

            # Untuk Linux gunakan xdg-open
            else:
                subprocess.Popen(["xdg-open", path])

        except Exception as e:

            # Tampilkan error jika gagal
            print(f"  Gagal membuka gambar: {e}")

    else:

        # File tidak ditemukan
        print(f"  File tidak ditemukan: {path}")


# ============================================================
# VIEWER UTAMA
# Menampilkan semua gambar dalam linked list dengan navigasi
# Fitur: Next, Prev, Quit
# ============================================================

def viewer_utama(dll):

    # Ubah linked list jadi list Python biasa
    nodes = dll.to_list()

    # Jika tidak ada gambar
    if not nodes:
        print("  Belum ada gambar untuk ditampilkan!")
        return

    # Mulai dari gambar pertama (index 0)
    index = 0
    total = len(nodes)

    while True:

        # Ambil node saat ini berdasarkan index
        current = nodes[index]

        # Tampilkan info gambar
        print("\n" + "=" * 50)
        print(f"  [VIEWER UTAMA] Gambar ke-{index + 1} dari {total}")
        print(f"  ID   : {current.id}")
        print(f"  Nama : {current.nama}")
        print(f"  Path : {current.path}")
        print("=" * 50)

        # Buka gambar dengan program default
        buka_gambar(current.path)

        # Tampilkan pilihan navigasi
        pilih = input("  [N] Next | [P] Prev | [Q] Quit Viewer : ").strip().lower()

        # NEXT: pindah ke gambar berikutnya
        if pilih == "n":

            # Jika belum di gambar terakhir, maju satu langkah
            if index < total - 1:
                index += 1

            # Jika sudah terakhir, kembali ke gambar pertama (circular)
            else:
                index = 0

        # PREV: kembali ke gambar sebelumnya
        elif pilih == "p":

            # Jika belum di gambar pertama, mundur satu langkah
            if index > 0:
                index -= 1

            # Jika sudah di gambar pertama, lompat ke gambar terakhir (circular)
            else:
                index = total - 1

        # QUIT: keluar dari viewer utama
        elif pilih == "q":
            print("  Keluar dari viewer utama.")
            break

        else:
            print("  Input tidak valid! Gunakan N, P, atau Q.")


# ============================================================
# VIEWER HASIL PENCARIAN  *** FITUR BARU ***
# Menampilkan hanya gambar hasil pencarian dengan navigasi
# dua arah layaknya Doubly Linked List.
#
# Parameter:
#   hasil  -> list of Node yang merupakan hasil pencarian
#
# Fitur navigasi:
#   N = Next  (maju, jika sudah terakhir balik ke pertama)
#   P = Prev  (mundur, jika sudah pertama lompat ke terakhir)
#   Q = Quit  (keluar dari viewer hasil pencarian)
# ============================================================

def viewer_search(hasil):

    # Jika hasil pencarian kosong, tidak perlu masuk viewer
    if not hasil:
        print("  Tidak ada gambar untuk ditampilkan!")
        return

    # Mulai dari hasil pertama (index 0)
    index = 0

    # Total gambar dalam hasil pencarian
    total = len(hasil)

    # Loop utama viewer hasil pencarian
    while True:

        # Ambil node hasil pencarian saat ini
        current = hasil[index]

        # Tampilkan header viewer hasil pencarian
        print("\n" + "=" * 50)
        print(f"  [VIEWER HASIL CARI] Gambar ke-{index + 1} dari {total}")
        print(f"  ID   : {current.id}")
        print(f"  Nama : {current.nama}")
        print(f"  Path : {current.path}")
        print("=" * 50)

        # Buka file gambar menggunakan fungsi buka_gambar yang sudah ada
        buka_gambar(current.path)

        # Tampilkan opsi navigasi khusus viewer hasil pencarian
        pilih = input("  [N] Next | [P] Prev | [Q] Quit Viewer : ").strip().lower()

        # NEXT: pindah ke hasil pencarian berikutnya
        if pilih == "n":

            # Jika masih ada hasil selanjutnya, maju satu langkah
            if index < total - 1:
                index += 1

            # Jika sudah di hasil terakhir, kembali ke hasil pertama (circular)
            else:
                index = 0
                print("  Sudah gambar terakhir, kembali ke awal.")

        # PREV: kembali ke hasil pencarian sebelumnya
        elif pilih == "p":

            # Jika masih ada hasil sebelumnya, mundur satu langkah
            if index > 0:
                index -= 1

            # Jika sudah di hasil pertama, lompat ke hasil terakhir (circular)
            else:
                index = total - 1
                print("  Sudah gambar pertama, lompat ke akhir.")

        # QUIT: keluar dari viewer hasil pencarian, kembali ke menu
        elif pilih == "q":
            print("  Keluar dari viewer hasil pencarian.")
            break

        # Input tidak dikenali
        else:
            print("  Input tidak valid! Gunakan N, P, atau Q.")


# ============================================================
# CARI GAMBAR
# Menu pencarian berdasarkan ID atau nama file.
# Setelah hasil ditemukan, user ditawarkan masuk ke
# viewer_search untuk preview otomatis hasil pencarian.
# ============================================================

def cari_gambar(dll):

    # Judul menu pencarian
    print("\n=== PENCARIAN GAMBAR ===")
    print("  1. Cari berdasarkan ID")
    print("  2. Cari berdasarkan Nama File")

    # Input metode pencarian
    metode = input("  Pilih metode pencarian: ").strip()

    # ========================================================
    # SEARCH BERDASARKAN ID
    # ========================================================

    if metode == "1":

        try:

            # Input ID target
            target_id = int(input("  Masukkan ID: "))

            # Cari node berdasarkan ID, hasilnya berupa list
            hasil = dll.search_by_id(target_id)

        except ValueError:

            # Jika input bukan angka
            print("  ID harus berupa angka!")
            return

    # ========================================================
    # SEARCH BERDASARKAN NAMA FILE
    # ========================================================

    elif metode == "2":

        # Input keyword pencarian (tanpa ekstensi)
        keyword = input("  Masukkan nama (tanpa ekstensi): ").strip()

        # Cari semua node yang namanya cocok, hasilnya berupa list
        hasil = dll.search_by_nama(keyword)

    else:

        # Jika pilihan tidak valid
        print("  Pilihan tidak valid!")
        return

    # ========================================================
    # TAMPILKAN HASIL PENCARIAN DALAM BENTUK TABEL
    # Tetap menampilkan tabel seperti sebelumnya
    # ========================================================

    print(f"\n  Ditemukan {len(hasil)} hasil:\n")

    # Cetak hasil dalam format tabel
    cetak_tabel(hasil)

    # ========================================================
    # TAWARAN BUKA VIEWER HASIL PENCARIAN  *** FITUR BARU ***
    # Hanya ditampilkan jika ada hasil yang ditemukan
    # ========================================================

    if hasil:

        # Tanya user apakah ingin masuk ke viewer hasil pencarian
        pilih = input("\n  Buka hasil di viewer? (y/n): ").strip().lower()

        # Jika user memilih "y", masuk ke viewer khusus hasil pencarian
        if pilih == "y":

            # Panggil viewer_search dengan daftar hasil pencarian
            # Viewer ini terpisah dari viewer utama dan hanya
            # menampilkan gambar-gambar hasil pencarian saja
            viewer_search(hasil)


# ============================================================
# LIHAT GAMBAR
# Menampilkan semua data gambar dalam tabel
# ============================================================

def lihat_gambar(dll):

    # Ubah linked list jadi list
    nodes = dll.to_list()

    # Judul menu
    print("\n=== DAFTAR GAMBAR ===")

    # Jika kosong
    if not nodes:

        # Tampilkan pesan
        print("  Belum ada gambar.")

    else:

        # Cetak tabel
        cetak_tabel(nodes)


# ============================================================
# TAMBAH GAMBAR
# ============================================================

def tambah_gambar(dll):

    # Tampilkan path default
    print(f"  Path default : {DEFAULT_PATH}")

    # Input nama file
    nama = input("  Masukkan nama gambar: ").strip()

    # Gabungkan path default + nama file
    path = os.path.join(DEFAULT_PATH, nama)

    # Jika file ada
    if os.path.exists(path):

        # Tambah ke linked list
        dll.append(nama, path)

        # Simpan ke file
        save_images(dll)

        # Pesan berhasil
        print("  Gambar berhasil ditambahkan!")

    else:

        # Jika file tidak ditemukan
        print(f"  File tidak ditemukan: {path}")


# ============================================================
# UPDATE GAMBAR
# ============================================================

def update_gambar(dll):

    # Judul menu
    print("\n=== UPDATE GAMBAR ===")

    # Tampilkan data
    lihat_gambar(dll)

    # Jika list kosong
    if not dll.head:
        return

    try:

        # Input ID yang ingin diupdate
        id_update = int(input("  Masukkan ID gambar yang ingin diupdate: "))

        # Jika ID tidak ada
        if not dll.find_by_id(id_update):

            # Tampilkan pesan
            print("  ID tidak ditemukan!")

            return

        # Tampilkan path default
        print(f"  Path default : {DEFAULT_PATH}")

        # Input nama baru
        nama_baru = input("  Masukkan nama gambar baru: ").strip()

        # Gabungkan path
        path_baru = os.path.join(DEFAULT_PATH, nama_baru)

        # Jika file ditemukan
        if os.path.exists(path_baru):

            # Update data
            dll.update_by_id(id_update, nama_baru, path_baru)

            # Simpan data
            save_images(dll)

            # Pesan berhasil
            print("  Berhasil diupdate!")

        else:

            # Jika file tidak ada
            print(f"  File tidak ditemukan: {path_baru}")

    # Jika input bukan angka
    except ValueError:

        # Tampilkan pesan error
        print("  Harus angka!")


# ============================================================
# HAPUS GAMBAR
# ============================================================

def hapus_gambar(dll):

    # Judul menu
    print("\n=== HAPUS GAMBAR ===")

    # Tampilkan data
    lihat_gambar(dll)

    # Jika list kosong
    if not dll.head:
        return

    try:

        # Input ID yang ingin dihapus
        id_hapus = int(input("  Masukkan ID gambar yang ingin dihapus: "))

        # Coba hapus node
        if dll.delete_by_id(id_hapus):

            # Simpan perubahan
            save_images(dll)

            # Pesan berhasil
            print("  Gambar berhasil dihapus!")

        else:

            # ID tidak ditemukan
            print("  ID tidak ditemukan!")

    # Jika input bukan angka
    except ValueError:

        # Tampilkan pesan error
        print("  Harus angka!")


# ============================================================
# MAIN
# Fungsi utama program - menu utama
# ============================================================

def main():

    # Inisialisasi Doubly Linked List
    dll = DoublyLinkedList()

    # Load data dari file database
    load_images(dll)

    # Loop menu utama
    while True:

        # Tampilkan menu utama
        print("\n======================================")
        print("  SELAMAT DATANG DI IMAGE REVIEWER ")
        print(" Sistem Pengelolaan & Viewer Gambar ")
        print("======================================")
        print("\n" + "=" * 40)
        print("   IMAGE REVIEWER ")
        print("=" * 40)
        print("  1. Lihat List gambar")
        print("  2. Tambah Gambar")
        print("  3. Update Gambar")
        print("  4. Hapus Gambar")
        print("  5. Cari Gambar")
        print("  6. Viewer")
        print("  0. Keluar")
        print("=" * 40)

        # Input pilihan menu
        pilih = input("  Pilih menu: ").strip()

        # Lihat semua gambar
        if pilih == "1":
            lihat_gambar(dll)

        # Tambah gambar baru
        elif pilih == "2":
            tambah_gambar(dll)

        # Update gambar
        elif pilih == "3":
            update_gambar(dll)

        # Hapus gambar
        elif pilih == "4":
            hapus_gambar(dll)

        # Cari gambar + preview otomatis hasil pencarian
        elif pilih == "5":
            cari_gambar(dll)

        # Viewer utama untuk semua gambar
        elif pilih == "6":
            viewer_utama(dll)

        # Keluar dari program
        elif pilih == "0":
            print("  Terima kasih! Program selesai.")
            break

        # Pilihan tidak valid
        else:
            print("  Pilihan tidak valid!")


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()