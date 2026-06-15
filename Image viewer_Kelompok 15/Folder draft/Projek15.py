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
# LIHAT GAMBAR
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