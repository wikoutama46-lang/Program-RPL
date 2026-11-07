from models.buku_model import BukuModel
from models.anggota_model import AnggotaModel

buku_model = BukuModel()
anggota_model = AnggotaModel()


def input_angka(pesan):
    while True:
        try:
            return int(input(pesan))
        except ValueError:
            print("Input harus berupa angka!")


def tampil_buku():
    data = buku_model.get_all_buku()
    print("\n=== Daftar Buku ===")
    print(f"{'ID':<5}{'Judul':<35}{'Penulis':<22}{'Tahun':<6}")
    print("-" * 68)
    for b in data:
        print(f"{b['id_buku']:<5}{b['judul']:<35}{b['penulis']:<22}{b['tahun_terbit']:<6}")
    print(f"Total: {len(data)} buku")


def tambah_buku():
    print("\n=== Tambah Buku ===")
    judul = input("Judul        : ")
    penulis = input("Penulis      : ")
    tahun = input_angka("Tahun terbit : ")
    if buku_model.create_buku(judul, penulis, tahun):
        print("Data buku berhasil ditambahkan!")
    else:
        print("Gagal menambahkan data buku.")


def ubah_buku():
    print("\n=== Ubah Buku ===")
    id_buku = input_angka("ID buku yang diubah : ")
    lama = buku_model.get_buku_by_id(id_buku)
    if not lama:
        print("Buku dengan ID tersebut tidak ditemukan.")
        return
    print(f"Data lama: {lama['judul']} | {lama['penulis']} | {lama['tahun_terbit']}")
    print("(Kosongkan lalu Enter untuk mempertahankan data lama)")
    judul = input("Judul baru        : ") or lama['judul']
    penulis = input("Penulis baru      : ") or lama['penulis']
    tahun_str = input("Tahun terbit baru : ")
    tahun = int(tahun_str) if tahun_str.isdigit() else lama['tahun_terbit']
    if buku_model.update_buku(id_buku, judul, penulis, tahun):
        print("Data buku berhasil diubah!")
    else:
        print("Gagal mengubah data buku.")


def hapus_buku():
    print("\n=== Hapus Buku ===")
    id_buku = input_angka("ID buku yang dihapus : ")
    lama = buku_model.get_buku_by_id(id_buku)
    if not lama:
        print("Buku dengan ID tersebut tidak ditemukan.")
        return
    print(f"Data: {lama['judul']} | {lama['penulis']} | {lama['tahun_terbit']}")
    yakin = input("Yakin hapus? (y/n) : ").lower()
    if yakin == "y":
        if buku_model.delete_buku(id_buku):
            print("Data buku berhasil dihapus!")
        else:
            print("Gagal menghapus data buku.")
    else:
        print("Penghapusan dibatalkan.")


def tampil_anggota():
    data = anggota_model.get_all_anggota()
    print("\n=== Daftar Anggota ===")
    print(f"{'ID':<5}{'Nama':<25}{'Alamat':<15}")
    print("-" * 45)
    for a in data:
        print(f"{a['id_anggota']:<5}{a['nama']:<25}{a['alamat']:<15}")
    print(f"Total: {len(data)} anggota")


def tambah_anggota():
    print("\n=== Tambah Anggota ===")
    nama = input("Nama   : ")
    alamat = input("Alamat : ")
    if anggota_model.create_anggota(nama, alamat):
        print("Data anggota berhasil ditambahkan!")
    else:
        print("Gagal menambahkan data anggota.")


def menu_buku():
    while True:
        print("\n--- MENU BUKU ---")
        print("1. Lihat semua buku")
        print("2. Tambah buku")
        print("3. Ubah buku")
        print("4. Hapus buku")
        print("0. Kembali")
        pilih = input("Pilih menu : ")
        if pilih == "1":
            tampil_buku()
        elif pilih == "2":
            tambah_buku()
        elif pilih == "3":
            ubah_buku()
        elif pilih == "4":
            hapus_buku()
        elif pilih == "0":
            break
        else:
            print("Pilihan tidak valid!")


def menu_anggota():
    while True:
        print("\n--- MENU ANGGOTA ---")
        print("1. Lihat semua anggota")
        print("2. Tambah anggota")
        print("0. Kembali")
        pilih = input("Pilih menu : ")
        if pilih == "1":
            tampil_anggota()
        elif pilih == "2":
            tambah_anggota()
        elif pilih == "0":
            break
        else:
            print("Pilihan tidak valid!")


def main():
    while True:
        print("\n==============================")
        print("   APLIKASI PERPUSTAKAAN")
        print("==============================")
        print("1. Kelola Buku")
        print("2. Kelola Anggota")
        print("0. Keluar")
        pilih = input("Pilih menu : ")
        if pilih == "1":
            menu_buku()
        elif pilih == "2":
            menu_anggota()
        elif pilih == "0":
            print("Terima kasih!")
            break
        else:
            print("Pilihan tidak valid!")


if __name__ == "__main__":
    main()