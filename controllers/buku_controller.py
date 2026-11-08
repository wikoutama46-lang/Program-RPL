import tkinter.messagebox as messagebox
from models.buku_model import BukuModel
from views.buku_view import BukuView


class BukuController:

    def __init__(self, user_role="admin"):
        self.user_role = str(user_role).lower()
        self.model = BukuModel()
        self.view = BukuView()

        # Atur Judul Window
        self.view.title(
            f"Sistem Manajemen Perpustakaan - Mode: {self.user_role.upper()}"
        )

        # Hanya role 'admin' atau 'petugas' yang diizinkan mengedit/menambah data
        is_admin = self.user_role in ["admin", "petugas"]

        if hasattr(self.view, "btn_simpan"):
            if is_admin:
                self.view.btn_simpan.configure(
                    state="normal",
                    text="Simpan Data",
                    command=self.simpan_data,
                )
            else:
                self.view.btn_simpan.configure(
                    state="disabled", text="Khusus Admin"
                )

        if hasattr(self.view, "btn_update"):
            if is_admin:
                self.view.btn_update.configure(
                    state="normal", command=self.update_data
                )
            else:
                self.view.btn_update.configure(state="disabled")

        if hasattr(self.view, "btn_delete"):
            if is_admin:
                self.view.btn_delete.configure(
                    state="normal", command=self.hapus_data
                )
            else:
                self.view.btn_delete.configure(state="disabled")

        if hasattr(self.view, "btn_logout"):
            self.view.btn_logout.configure(command=self.logout)

        # Binding seleksi tabel
        tabel_widget = getattr(
            self.view, "tabel", getattr(self.view, "tree", None)
        )
        if tabel_widget:
            tabel_widget.bind("<<TreeviewSelect>>", self.on_select_tabel)

        self.muat_data_tabel()

    def muat_data_tabel(self):
        tabel_widget = getattr(
            self.view, "tabel", getattr(self.view, "tree", None)
        )
        if tabel_widget is not None:
            for item in tabel_widget.get_children():
                tabel_widget.delete(item)

            data_buku = self.model.get_all_buku()
            if data_buku:
                for buku in data_buku:
                    if isinstance(buku, dict):
                        tabel_widget.insert(
                            "",
                            "end",
                            values=(
                                buku.get("id_buku"),
                                buku.get("judul"),
                                buku.get("penulis"),
                                buku.get("tahun_terbit"),
                            ),
                        )
                    else:
                        tabel_widget.insert("", "end", values=buku)

    def on_select_tabel(self, event):
        tabel_widget = getattr(
            self.view, "tabel", getattr(self.view, "tree", None)
        )
        selected_item = tabel_widget.selection()
        if selected_item:
            item_data = tabel_widget.item(selected_item[0])["values"]
            if hasattr(self.view, "entry_judul"):
                self.view.entry_judul.delete(0, "end")
                self.view.entry_judul.insert(0, item_data[1])

            if hasattr(self.view, "entry_penulis"):
                self.view.entry_penulis.delete(0, "end")
                self.view.entry_penulis.insert(0, item_data[2])

            if hasattr(self.view, "entry_tahun"):
                self.view.entry_tahun.delete(0, "end")
                self.view.entry_tahun.insert(0, item_data[3])

    def simpan_data(self):
        if self.user_role not in ["admin", "petugas"]:
            messagebox.showerror(
                "Akses Ditolak", "Anda tidak memiliki izin untuk menambah data!"
            )
            return

        judul = self.view.entry_judul.get().strip()
        penulis = self.view.entry_penulis.get().strip()
        tahun = self.view.entry_tahun.get().strip()

        if not judul or not penulis or not tahun:
            messagebox.showwarning(
                "Peringatan", "Semua kolom form harus diisi!"
            )
            return

        if self.model.create_buku(judul, penulis, tahun):
            messagebox.showinfo("Sukses", "Data buku berhasil disimpan!")
            self.kosongkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Gagal menyimpan data.")

    def update_data(self):
        if self.user_role not in ["admin", "petugas"]:
            messagebox.showerror(
                "Akses Ditolak", "Anda tidak memiliki izin untuk mengedit data!"
            )
            return

        tabel_widget = getattr(
            self.view, "tabel", getattr(self.view, "tree", None)
        )
        selected_item = tabel_widget.selection()

        if not selected_item:
            messagebox.showwarning(
                "Peringatan", "Pilih baris buku di tabel yang ingin diperbarui!"
            )
            return

        id_buku = tabel_widget.item(selected_item[0])["values"][0]
        judul = self.view.entry_judul.get().strip()
        penulis = self.view.entry_penulis.get().strip()
        tahun = self.view.entry_tahun.get().strip()

        if hasattr(self.model, "update_buku"):
            if self.model.update_buku(id_buku, judul, penulis, tahun):
                messagebox.showinfo("Sukses", "Data buku berhasil diperbarui!")
                self.kosongkan_form()
                self.muat_data_tabel()
            else:
                messagebox.showerror("Error", "Gagal memperbarui data buku.")

    def hapus_data(self):
        if self.user_role not in ["admin", "petugas"]:
            messagebox.showerror(
                "Akses Ditolak", "Anda tidak memiliki izin untuk menghapus data!"
            )
            return

        tabel_widget = getattr(
            self.view, "tabel", getattr(self.view, "tree", None)
        )
        selected_item = tabel_widget.selection()

        if not selected_item:
            messagebox.showwarning(
                "Peringatan", "Pilih baris buku di tabel yang ingin dihapus!"
            )
            return

        id_buku = tabel_widget.item(selected_item[0])["values"][0]
        konfirmasi = messagebox.askyesno(
            "Konfirmasi Hapus",
            f"Apakah Anda yakin ingin menghapus buku ID {id_buku}?",
        )

        if konfirmasi:
            if hasattr(self.model, "delete_buku"):
                if self.model.delete_buku(id_buku):
                    messagebox.showinfo("Sukses", "Data buku berhasil dihapus!")
                    self.kosongkan_form()
                    self.muat_data_tabel()
                else:
                    messagebox.showerror("Error", "Gagal menghapus data.")

    def logout(self):
        konfirmasi = messagebox.askyesno(
            "Konfirmasi Logout", "Apakah Anda yakin ingin keluar?"
        )
        if konfirmasi:
            self.view.destroy()
            from controllers.auth_controller import AuthController

            self.auth_app = AuthController()
            self.auth_app.run()

    def kosongkan_form(self):
        if hasattr(self.view, "entry_judul"):
            self.view.entry_judul.delete(0, "end")
        if hasattr(self.view, "entry_penulis"):
            self.view.entry_penulis.delete(0, "end")
        if hasattr(self.view, "entry_tahun"):
            self.view.entry_tahun.delete(0, "end")

    def run(self):
        self.view.mainloop()