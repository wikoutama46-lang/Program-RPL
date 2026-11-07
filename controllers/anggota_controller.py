import tkinter.messagebox as messagebox
from models.anggota_model import AnggotaModel
from views.anggota_view import AnggotaView

class AnggotaController:
    def __init__(self):
        # Inisialisasi Model dan View
        self.model = AnggotaModel()
        self.view = AnggotaView()

        # Binding (mengikat) tombol di View dengan fungsi di Controller
        self.view.btn_simpan.configure(command=self.simpan_data)
        self.view.btn_perbarui.configure(command=self.perbarui_data)
        self.view.btn_hapus.configure(command=self.hapus_data)

        # Menyimpan id_anggota dari baris tabel yang diklik pengguna
        self.id_terpilih = None
        self.view.tabel.bind("<<TreeviewSelect>>", self.pilih_data)

        # Memuat data ke tabel saat aplikasi pertama kali dibuka
        self.muat_data_tabel()

    def muat_data_tabel(self):
        # Mengosongkan isi tabel di View terlebih dahulu
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)

        # Mengambil data dari Model (database)
        data_anggota = self.model.get_all_anggota()

        # Memasukkan data baru ke dalam tabel View
        for anggota in data_anggota:
            self.view.tabel.insert(
                "", "end",
                values=(
                    anggota['id_anggota'],
                    anggota['nama'],
                    anggota['alamat']
                )
            )

    def bersihkan_form(self):
        # Kosongkan form input dan lepas pilihan baris
        self.view.entry_nama.delete(0, 'end')
        self.view.entry_alamat.delete(0, 'end')
        self.id_terpilih = None

    def pilih_data(self, event=None):
        # Dipanggil saat pengguna mengklik baris tabel
        pilihan = self.view.tabel.selection()
        if not pilihan:
            return
        nilai = self.view.tabel.item(pilihan[0], "values")

        # Ambil id_anggota dari baris yang diklik, lalu isi form dengan datanya
        self.bersihkan_form()
        self.id_terpilih = nilai[0]
        self.view.entry_nama.insert(0, nilai[1])
        self.view.entry_alamat.insert(0, nilai[2])

    def simpan_data(self):
        # Mengambil teks dari kotak input di View
        nama = self.view.entry_nama.get()
        alamat = self.view.entry_alamat.get()

        # Validasi Form Kosong
        if not nama or not alamat:
            messagebox.showwarning(
                "Peringatan",
                "Semua kolom form harus diisi!"
            )
            return

        # Mengirim data ke Model untuk disimpan
        berhasil = self.model.create_anggota(nama, alamat)
        if berhasil:
            messagebox.showinfo(
                "Sukses",
                "Data anggota berhasil disimpan!"
            )
            self.bersihkan_form()
            # Muat ulang tabel agar data terbaru muncul
            self.muat_data_tabel()
        else:
            messagebox.showerror(
                "Error",
                "Terjadi kesalahan saat menyimpan data."
            )

    def perbarui_data(self):
        # Pastikan ada baris yang dipilih di tabel
        if self.id_terpilih is None:
            messagebox.showwarning(
                "Peringatan",
                "Pilih data anggota pada tabel terlebih dahulu!"
            )
            return

        nama = self.view.entry_nama.get()
        alamat = self.view.entry_alamat.get()

        # Validasi Form Kosong
        if not nama or not alamat:
            messagebox.showwarning(
                "Peringatan",
                "Semua kolom form harus diisi!"
            )
            return

        # Teruskan id_anggota beserta data baru ke fungsi update di Model
        berhasil = self.model.update_anggota(self.id_terpilih, nama, alamat)
        if berhasil:
            messagebox.showinfo(
                "Sukses",
                "Data anggota berhasil diperbarui!"
            )
            self.bersihkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror(
                "Error",
                "Terjadi kesalahan saat memperbarui data."
            )

    def hapus_data(self):
        # Pastikan ada baris yang dipilih di tabel
        if self.id_terpilih is None:
            messagebox.showwarning(
                "Peringatan",
                "Pilih data anggota pada tabel terlebih dahulu!"
            )
            return

        # Minta konfirmasi sebelum data dihapus
        yakin = messagebox.askyesno(
            "Konfirmasi",
            "Yakin ingin menghapus data anggota ini?"
        )
        if not yakin:
            return

        # Teruskan id_anggota ke fungsi hapus di Model
        berhasil = self.model.delete_anggota(self.id_terpilih)
        if berhasil:
            messagebox.showinfo(
                "Sukses",
                "Data anggota berhasil dihapus!"
            )
            self.bersihkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror(
                "Error",
                "Terjadi kesalahan saat menghapus data."
            )

    # Fungsi untuk menjalankan aplikasi
    def run(self):
        self.view.mainloop()
