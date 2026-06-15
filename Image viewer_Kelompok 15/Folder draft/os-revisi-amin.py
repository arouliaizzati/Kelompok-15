import os
import subprocess

# ============================================================
# KONFIGURASI
# ============================================================
FILE_DB      = "images.txt"
DEFAULT_PATH = "C:\\image"

# ============================================================
# STRUKTUR DATA: NODE
# Setiap gambar disimpan sebagai satu Node dalam linked list.
# Setiap Node menyimpan pointer ke node sebelumnya (prev)
# dan node sesudahnya (next) — itulah yang membuat struktur
# ini disebut "Doubly" (dua arah).
# ============================================================
class Node:
    def __init__(self, id, nama, path):
        self.id   = id        # ID unik gambar
        self.nama = nama      # Nama file gambar
        self.path = path      # Path lengkap gambar
        self.next = None      # Pointer ke node berikutnya
        self.prev = None      # Pointer ke node sebelumnya

# ============================================================
# STRUKTUR DATA: DOUBLY LINKED LIST
# Mengelola seluruh koleksi Node. Head = node pertama,
# tail = node terakhir. Traversal bisa dilakukan dua arah.
# ============================================================
class DoublyLinkedList:
    def __init__(self):
        self.head    = None   # Node pertama dalam list
        self.tail    = None   # Node terakhir dalam list
        self._id_seq = 1      # Auto-increment ID

    # --------------------------------------------------------
    # APPEND: Tambah node baru di akhir list
    # --------------------------------------------------------
    def append(self, nama, path, id=None):
        node_id = id if id is not None else self._id_seq
        # Pastikan _id_seq selalu lebih besar dari ID yang ada
        if node_id >= self._id_seq:
            self._id_seq = node_id + 1

        new_node = Node(node_id, nama, path)

        if self.head is None:           # List masih kosong
            self.head = new_node
            self.tail = new_node
        else:                           # Sambung ke tail
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail       = new_node

        return new_node

    # --------------------------------------------------------
    # FIND BY ID: Cari node berdasarkan ID (traversal linear)
    # --------------------------------------------------------
    def find_by_id(self, target_id):
        cur = self.head
        while cur:
            if cur.id == target_id:
                return cur
            cur = cur.next
        return None

    # --------------------------------------------------------
    # UPDATE BY ID: Ganti nama & path node tertentu
    # --------------------------------------------------------
    def update_by_id(self, target_id, nama_baru, path_baru):
        node = self.find_by_id(target_id)
        if node:
            node.nama = nama_baru
            node.path = path_baru
            return True
        return False

    # --------------------------------------------------------
    # DELETE BY ID: Putus pointer prev/next lalu lepas node
    # --------------------------------------------------------
    def delete_by_id(self, target_id):
        node = self.find_by_id(target_id)
        if not node:
            return False

        # Hubungkan ulang node sebelum dan sesudahnya
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next   # Node yang dihapus adalah head

        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev   # Node yang dihapus adalah tail

        node.prev = None
        node.next = None
        return True

    # --------------------------------------------------------
    # TO LIST: Konversi linked list ke list Python biasa
    # (dipakai untuk save ke file)
    # --------------------------------------------------------
    def to_list(self):
        result = []
        cur = self.head
        while cur:
            result.append(cur)
            cur = cur.next
        return result

    # --------------------------------------------------------
    # SEARCH BY ID: Kembalikan list node yang ID-nya cocok
    # --------------------------------------------------------
    def search_by_id(self, target_id):
        node = self.find_by_id(target_id)
        return [node] if node else []

    # --------------------------------------------------------
    # SEARCH BY NAMA: Case-insensitive, tanpa perlu ekstensi
    # --------------------------------------------------------
    def search_by_nama(self, keyword):
        keyword = keyword.lower()
        hasil   = []
        cur     = self.head
        while cur:
            # Bandingkan keyword dengan nama file (tanpa ekstensi)
            nama_tanpa_ext = os.path.splitext(cur.nama)[0].lower()
            if keyword in nama_tanpa_ext or keyword in cur.nama.lower():
                hasil.append(cur)
            cur = cur.next
        return hasil

# ============================================================
# LOAD & SAVE
# ============================================================
def load_images(dll):
    if not os.path.exists(FILE_DB):
        open(FILE_DB, "w").close()

    with open(FILE_DB, "r") as f:
        for line in f:
            if line.strip():
                parts = line.strip().split("|")
                if len(parts) == 3:
                    id_, nama, path = parts
                    dll.append(nama, path, id=int(id_))

def save_images(dll):
    with open(FILE_DB, "w") as f:
        for node in dll.to_list():
            f.write(f"{node.id}|{node.nama}|{node.path}\n")

# ============================================================
# TAMPILAN TABEL
# ============================================================
def cetak_tabel(nodes):
    if not nodes:
        print("  Data tidak ditemukan.")
        return

    # Hitung lebar kolom secara dinamis
    col_id   = max(len(str(n.id))   for n in nodes)
    col_id   = max(col_id, 2)
    col_nama = max(len(n.nama)      for n in nodes)
    col_nama = max(col_nama, len("Nama Gambar"))
    col_path = max(len(n.path)      for n in nodes)
    col_path = max(col_path, len("Path Gambar"))

    sep    = f"+{'-'*(col_id+2)}+{'-'*(col_nama+2)}+{'-'*(col_path+2)}+"
    header = (f"| {'ID'.center(col_id)} "
              f"| {'Nama Gambar'.ljust(col_nama)} "
              f"| {'Path Gambar'.ljust(col_path)} |")

    print(sep)
    print(header)
    print(sep)
    for n in nodes:
        print(f"| {str(n.id).center(col_id)} "
              f"| {n.nama.ljust(col_nama)} "
              f"| {n.path.ljust(col_path)} |")
    print(sep)

# ============================================================
# CRUD
# ============================================================
def lihat_gambar(dll):
    nodes = dll.to_list()
    print("\n=== DAFTAR GAMBAR ===")
    if not nodes:
        print("  Belum ada gambar.")
    else:
        cetak_tabel(nodes)

def tambah_gambar(dll):
    print(f"  Path default : {DEFAULT_PATH}")
    nama = input("  Masukkan nama gambar: ").strip()
    path = os.path.join(DEFAULT_PATH, nama)

    if os.path.exists(path):
        dll.append(nama, path)
        save_images(dll)
        print("  Gambar berhasil ditambahkan!")
    else:
        print(f"  File tidak ditemukan: {path}")

def update_gambar(dll):
    print("\n=== UPDATE GAMBAR ===")
    lihat_gambar(dll)
    if not dll.head:
        return

    try:
        id_update = int(input("  Masukkan ID gambar yang ingin diupdate: "))
        if not dll.find_by_id(id_update):
            print("  ID tidak ditemukan!")
            return

        print(f"  Path default : {DEFAULT_PATH}")
        nama_baru = input("  Masukkan nama gambar baru: ").strip()
        path_baru = os.path.join(DEFAULT_PATH, nama_baru)

        if os.path.exists(path_baru):
            dll.update_by_id(id_update, nama_baru, path_baru)
            save_images(dll)
            print("  Berhasil diupdate!")
        else:
            print(f"  File tidak ditemukan: {path_baru}")
    except ValueError:
        print("  Harus angka!")

def hapus_gambar(dll):
    print("\n=== HAPUS GAMBAR ===")
    lihat_gambar(dll)
    if not dll.head:
        return

    try:
        id_hapus = int(input("  Masukkan ID gambar yang ingin dihapus: "))
        if dll.delete_by_id(id_hapus):
            save_images(dll)
            print("  Berhasil dihapus!")
        else:
            print("  ID tidak ditemukan!")
    except ValueError:
        print("  Harus angka!")

# ============================================================
# SEARCHING
# ============================================================
def cari_gambar(dll):
    print("\n=== PENCARIAN GAMBAR ===")
    print("  1. Cari berdasarkan ID")
    print("  2. Cari berdasarkan Nama File")
    metode = input("  Pilih metode pencarian: ").strip()

    if metode == "1":
        try:
            target_id = int(input("  Masukkan ID: "))
            hasil     = dll.search_by_id(target_id)
        except ValueError:
            print("  Harus angka!")
            return

    elif metode == "2":
        keyword = input("  Masukkan nama (tanpa ekstensi): ").strip()
        hasil   = dll.search_by_nama(keyword)

    else:
        print("  Pilihan tidak valid!")
        return

    print(f"\n  Ditemukan {len(hasil)} hasil:\n")
    cetak_tabel(hasil)

# ============================================================
# MEMBUKA GAMBAR
# ============================================================
def buka_gambar(path):
    try:
        if os.name == "nt":
            os.startfile(path)
        elif os.name == "posix":
            subprocess.run(["xdg-open", path])
        else:
            print("  OS tidak didukung.")
    except Exception as e:
        print("  Gagal membuka gambar:", e)

# ============================================================
# VIEWER — memanfaatkan pointer node.next / node.prev
# ============================================================
def viewer(dll):
    if not dll.head:
        print("  Tidak ada gambar!")
        return

    # Mulai dari node pertama (head)
    current = dll.head
    total   = len(dll.to_list())
    index   = 1

    while True:
        print("\n===================")
        print(f"  Gambar ke-{index}/{total}")
        print(f"  ID   : {current.id}")
        print(f"  Nama : {current.nama}")
        print(f"  Path : {current.path}")
        print("===================")

        buka_gambar(current.path)
        pilih = input("  [N] Next | [P] Prev | [Q] Quit : ").lower()

        if pilih == "n":
            if current.next:             # Ada node sesudahnya
                current = current.next
                index  += 1
            else:                        # Sudah di akhir, balik ke head
                current = dll.head
                index   = 1

        elif pilih == "p":
            if current.prev:             # Ada node sebelumnya
                current = current.prev
                index  -= 1
            else:                        # Sudah di awal, loncat ke tail
                current = dll.tail
                index   = total

        elif pilih == "q":
            break
        else:
            print("  Input salah!")

# ============================================================
# MENU UTAMA
# ============================================================
def main():
    dll = DoublyLinkedList()
    load_images(dll)

    while True:
        print("\n======================================")
        print("  SELAMAT DATANG DI IMAGE REVIEWER ")
        print(" Sistem Pengelolaan & Viewer Gambar ")
        print("======================================")

        print("\n====== IMAGE REVIEWER ======")
        print("  1. Lihat Data")
        print("  2. Tambah Gambar")
        print("  3. Update Gambar")
        print("  4. Hapus Gambar")
        print("  5. Pencarian Gambar")
        print("  6. Viewer")
        print("  7. Keluar")

        pilih = input("  Pilih menu: ")

        if   pilih == "1": lihat_gambar(dll)
        elif pilih == "2": tambah_gambar(dll)
        elif pilih == "3": update_gambar(dll)
        elif pilih == "4": hapus_gambar(dll)
        elif pilih == "5": cari_gambar(dll)
        elif pilih == "6": viewer(dll)
        elif pilih == "7":
            print("  Program selesai.")
            break
        else:
            print("  Menu tidak valid!")

main()
