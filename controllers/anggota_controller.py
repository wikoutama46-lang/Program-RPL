import tkinter.messagebox as messagebox
from models.anggota_model import AnggotaModel
from views.anggota_view import AnggotaView

class AnggotaController:
    def __init__(self, view=None, model=None):
        # Mendukung pemanggilan tanpa parameter atau dengan parameter (app, model)
        self.model = model if model else AnggotaModel()
        self.view = view if view else AnggotaView()
        self.selected_id = None

        # 1. Binding Tombol Simpan
        if hasattr(self.view, 'btn_simpan'):
            self.view.btn_simpan.configure(command=self.simpan_data)

        # 2. Binding Tombol Perbarui / Update
        if hasattr(self.view, 'btn_perbarui'):
            self.view.btn_perbarui.configure(command=self.perbarui_data)
        elif hasattr(self.view, 'btn_update'):
            self.view.btn_update.configure(command=self.perbarui_data)

        # 3. Binding Tombol Hapus / Delete
        if hasattr(self.view, 'btn_hapus'):
            self.view.btn_hapus.configure(command=self.hapus_data)
        elif hasattr(self.view, 'btn_delete'):
            self.view.btn_delete.configure(command=self.hapus_data)

        # 4. Binding Event Klik Baris pada Tabel
        if hasattr(self.view, 'tabel'):
            self.view.tabel.bind("<<TreeviewSelect>>", self.pada_baris_diklik)

        self.muat_data_tabel()

    def muat_data_tabel(self):
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)

        data_anggota = self.model.get_all_anggota()
        for anggota in data_anggota:
            id_val = anggota.get('id_anggota') or anggota.get('id')
            nama_val = anggota.get('nama') or anggota.get('nama_lengkap') or anggota.get('nama_anggota')
            alamat_val = anggota.get('alamat') or anggota.get('Alamat') or "-"

            self.view.tabel.insert(
                "",
                "end",
                values=(
                    id_val,
                    nama_val,
                    alamat_val
                )
            )

    def pada_baris_diklik(self, event):
        selected_item = self.view.tabel.selection()
        if selected_item:
            item_data = self.view.tabel.item(selected_item[0])['values']
            self.selected_id = int(str(item_data[0]).strip())
            
            if hasattr(self.view, 'entry_nama'):
                self.view.entry_nama.delete(0, 'end')
                self.view.entry_nama.insert(0, str(item_data[1]))
                
            if hasattr(self.view, 'entry_alamat'):
                self.view.entry_alamat.delete(0, 'end')
                self.view.entry_alamat.insert(0, str(item_data[2]))

    def simpan_data(self):
        nama = self.view.entry_nama.get() if hasattr(self.view, 'entry_nama') else ""
        alamat = self.view.entry_alamat.get() if hasattr(self.view, 'entry_alamat') else ""

        if not nama or not alamat:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")
            return

        berhasil = self.model.create_anggota(nama, alamat)
        if berhasil:
            messagebox.showinfo("Sukses", "Data anggota berhasil disimpan!")
            self.bersihkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Terjadi kesalahan saat menyimpan data.")

    def perbarui_data(self):
        if self.selected_id is None:
            messagebox.showwarning("Peringatan", "Klik/pilih salah satu baris anggota di tabel terlebih dahulu!")
            return

        nama = self.view.entry_nama.get() if hasattr(self.view, 'entry_nama') else ""
        alamat = self.view.entry_alamat.get() if hasattr(self.view, 'entry_alamat') else ""

        if not nama or not alamat:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")
            return

        berhasil = self.model.update_anggota(self.selected_id, nama, alamat)
        if berhasil:
            messagebox.showinfo("Sukses", "Data anggota berhasil diperbarui!")
            self.bersihkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Gagal memperbarui data anggota.")

    def hapus_data(self):
        if self.selected_id is None:
            messagebox.showwarning("Peringatan", "Klik/pilih salah satu baris anggota di tabel terlebih dahulu!")
            return

        konfirmasi = messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus data anggota ini?")
        if konfirmasi:
            berhasil = self.model.delete_anggota(self.selected_id)
            if berhasil:
                messagebox.showinfo("Sukses", "Data anggota berhasil dihapus!")
                self.bersihkan_form()
                self.muat_data_tabel()
            else:
                messagebox.showerror("Error", "Gagal menghapus data anggota.")

    def bersihkan_form(self):
        self.selected_id = None
        if hasattr(self.view, 'entry_nama'):
            self.view.entry_nama.delete(0, 'end')
        if hasattr(self.view, 'entry_alamat'):
            self.view.entry_alamat.delete(0, 'end')

    def run(self):
        self.view.mainloop()