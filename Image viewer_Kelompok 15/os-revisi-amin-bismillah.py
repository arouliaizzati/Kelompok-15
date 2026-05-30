from colorama import Fore, Style
from tabulate import tabulate
from pyfiglet import Figlet

import os
import subprocess
import textwrap

# ============================================================
# KONFIGURASI
# ============================================================
FILE_DB      = "images.txt"
DEFAULT_PATH = "C:\\image"

# ============================================================
# HELPER TAMPILAN
# ============================================================
LEBAR_FRAME = 72

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def garis(char="=", lebar=LEBAR_FRAME):
    return char * lebar

def judul(teks, warna=Fore.CYAN):
    print(warna + garis("=") + Style.RESET_ALL)
    print(warna + teks.center(LEBAR_FRAME) + Style.RESET_ALL)
    print(warna + garis("=") + Style.RESET_ALL)

def panel(teks, warna=Fore.WHITE):
    print(warna + garis("-") + Style.RESET_ALL)
    for baris in teks:
        isi_baris = textwrap.wrap(baris, width=LEBAR_FRAME - 4) or [""]
        for isi in isi_baris:
            print(warna + f"| {isi.ljust(LEBAR_FRAME - 4)} |" + Style.RESET_ALL)
    print(warna + garis("-") + Style.RESET_ALL)

def pesan(teks, warna=Fore.WHITE):
    panel([teks], warna)

def tunggu_enter():
    input(Fore.MAGENTA + "\n  Tekan Enter untuk kembali ke menu utama..." + Style.RESET_ALL)

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
        pesan("Data tidak ditemukan.", Fore.RED)
        return

    data = [[n.id, n.nama, n.path] for n in nodes]
    print(Fore.CYAN + tabulate(
        data,
        headers=["ID", "Nama Gambar", "Path Gambar"],
        tablefmt="fancy_grid",
        stralign="left",
        numalign="center"
    ) + Style.RESET_ALL)

# ============================================================
# CRUD
# ============================================================
def lihat_gambar(dll):
    nodes = dll.to_list()
    print()
    judul("DAFTAR GAMBAR", Fore.CYAN)
    if not nodes:
        pesan("Belum ada gambar.", Fore.YELLOW)
    else:
        cetak_tabel(nodes)

def tambah_gambar(dll):
    print()
    judul("TAMBAH GAMBAR", Fore.GREEN)
    panel([
        f"Path default : {DEFAULT_PATH}",
        "Masukkan nama file gambar yang ada di folder default."
    ], Fore.GREEN)
    nama = input(Fore.MAGENTA + "  Masukkan nama gambar: " + Style.RESET_ALL).strip()
    path = os.path.join(DEFAULT_PATH, nama)

    if os.path.exists(path):
        dll.append(nama, path)
        save_images(dll)
        pesan("Gambar berhasil ditambahkan!", Fore.GREEN)
    else:
        pesan(f"File tidak ditemukan: {path}", Fore.RED)

def update_gambar(dll):
    print()
    judul("UPDATE GAMBAR", Fore.YELLOW)
    lihat_gambar(dll)
    if not dll.head:
        return

    try:
        id_update = int(input(Fore.MAGENTA + "  Masukkan ID gambar yang ingin diupdate: " + Style.RESET_ALL))
        if not dll.find_by_id(id_update):
            pesan("ID tidak ditemukan!", Fore.RED)
            return

        panel([f"Path default : {DEFAULT_PATH}"], Fore.YELLOW)
        nama_baru = input(Fore.MAGENTA + "  Masukkan nama gambar baru: " + Style.RESET_ALL).strip()
        path_baru = os.path.join(DEFAULT_PATH, nama_baru)

        if os.path.exists(path_baru):
            dll.update_by_id(id_update, nama_baru, path_baru)
            save_images(dll)
            pesan("Gambar berhasil diupdate!", Fore.GREEN)
        else:
            pesan(f"File tidak ditemukan: {path_baru}", Fore.RED)
    except ValueError:
        pesan("Input ID harus berupa angka!", Fore.RED)

def hapus_gambar(dll):
    print()
    judul("HAPUS GAMBAR", Fore.RED)
    lihat_gambar(dll)
    if not dll.head:
        return

    try:
        id_hapus = int(input(Fore.MAGENTA + "  Masukkan ID gambar yang ingin dihapus: " + Style.RESET_ALL))
        if dll.delete_by_id(id_hapus):
            save_images(dll)
            pesan("Gambar berhasil dihapus!", Fore.GREEN)
        else:
            pesan("ID tidak ditemukan!", Fore.RED)
    except ValueError:
        pesan("Input ID harus berupa angka!", Fore.RED)

# ============================================================
# SEARCHING
# ============================================================
def cari_gambar(dll):
    print()
    judul("PENCARIAN GAMBAR", Fore.BLUE)
    panel([
        "1. Cari berdasarkan ID",
        "2. Cari berdasarkan Nama File"
    ], Fore.BLUE)
    metode = input(Fore.MAGENTA + "  Pilih metode pencarian: " + Style.RESET_ALL).strip()

    if metode == "1":
        try:
            target_id = int(input(Fore.MAGENTA + "  Masukkan ID: " + Style.RESET_ALL))
            hasil     = dll.search_by_id(target_id)
        except ValueError:
            pesan("Input ID harus berupa angka!", Fore.RED)
            return

    elif metode == "2":
        keyword = input(Fore.MAGENTA + "  Masukkan nama (tanpa ekstensi): " + Style.RESET_ALL).strip()
        hasil   = dll.search_by_nama(keyword)

    else:
        pesan("Pilihan tidak valid!", Fore.RED)
        return

    print()
    pesan(f"Ditemukan {len(hasil)} hasil.", Fore.GREEN if hasil else Fore.YELLOW)
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
            pesan("OS tidak didukung.", Fore.RED)
    except Exception as e:
        pesan(f"Gagal membuka gambar: {e}", Fore.RED)

# ============================================================
# VIEWER — memanfaatkan pointer node.next / node.prev
# ============================================================
def viewer(dll):
    if not dll.head:
        pesan("Tidak ada gambar!", Fore.RED)
        return

    # Mulai dari node pertama (head)
    current = dll.head
    total   = len(dll.to_list())
    index   = 1

    while True:
        print()
        judul("VIEWER GAMBAR", Fore.MAGENTA)
        panel([
            f"Gambar ke-{index}/{total}",
            f"ID   : {current.id}",
            f"Nama : {current.nama}",
            f"Path : {current.path}"
        ], Fore.MAGENTA)

        buka_gambar(current.path)
        pilih = input(Fore.MAGENTA + "  [N] Next | [P] Prev | [Q] Quit : " + Style.RESET_ALL).lower()

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
            pesan("Input salah! Gunakan N, P, atau Q.", Fore.RED)

# ============================================================
# MENU UTAMA
# ============================================================
def main():
    dll = DoublyLinkedList()
    load_images(dll)

    f = Figlet(font="small", width=LEBAR_FRAME)
    while True:
        clear_screen()
        print(Fore.YELLOW + f.renderText("Image Viewer") + Style.RESET_ALL)
        print(Fore.GREEN + " Sistem Pengelolaan & Viewer Gambar ".center(LEBAR_FRAME) + Style.RESET_ALL)
        print(Fore.GREEN + garis("=") + Style.RESET_ALL)

        panel([
            "MENU UTAMA",
            "",
            "1. Lihat Data",
            "2. Tambah Gambar",
            "3. Update Gambar",
            "4. Hapus Gambar",
            "5. Pencarian Gambar",
            "6. Viewer",
            "7. Keluar"
        ], Fore.CYAN)

        pilih = input(Fore.MAGENTA + "  Pilih menu: " + Style.RESET_ALL)

        if   pilih == "1": lihat_gambar(dll); tunggu_enter()
        elif pilih == "2": tambah_gambar(dll); tunggu_enter()
        elif pilih == "3": update_gambar(dll); tunggu_enter()
        elif pilih == "4": hapus_gambar(dll); tunggu_enter()
        elif pilih == "5": cari_gambar(dll); tunggu_enter()
        elif pilih == "6": viewer(dll); tunggu_enter()
        elif pilih == "7":
            pesan("Program selesai. Terima kasih!", Fore.RED)
            break
        else:
            pesan("Menu tidak valid!", Fore.RED)
            tunggu_enter()

main()
