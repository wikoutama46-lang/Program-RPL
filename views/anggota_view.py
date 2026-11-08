import customtkinter as ctk
from tkinter import ttk
from models.buku_model import BukuModel


class AnggotaView(ctk.CTk):

    def __init__(self, nama_user="Wiko Brenton Askelon Mangoli", nim="F5212530098"):
        super().__init__()

        self.nama_user = nama_user
        self.nim = nim
        self.model_buku = BukuModel()

        self.title("Sistem Manajemen Perpustakaan - Mode: ANGGOTA")
        self.geometry("900x550")

        self.setup_ui()
        self.load_data_buku()

    def setup_ui(self):
        # Frame Kiri (Form Input & Tombol Disabled)
        self.left_frame = ctk.CTkFrame(self, width=300)
        self.left_frame.pack(side="left", fill="y", padx=10, pady=10)

        ctk.CTkLabel(
            self.left_frame, text="Form Data Buku", font=("Arial", 16, "bold")
        ).pack(pady=15)

        self.entry_judul = ctk.CTkEntry(
            self.left_frame, placeholder_text="Masukkan Judul Buku", width=250
        )
        self.entry_judul.pack(pady=10)

        self.entry_penulis = ctk.CTkEntry(
            self.left_frame, placeholder_text="Masukkan Nama Penulis", width=250
        )
        self.entry_penulis.pack(pady=10)

        self.entry_tahun = ctk.CTkEntry(
            self.left_frame, placeholder_text="Tahun Terbit (Misal: 2024)", width=250
        )
        self.entry_tahun.pack(pady=10)

        # Tombol Khusus Admin (Disabled)
        self.btn_simpan = ctk.CTkButton(
            self.left_frame,
            text="Khusus Admin",
            fg_color="green",
            state="disabled",
            width=250,
            height=40,
        )
        self.btn_simpan.pack(pady=10)

        self.btn_update = ctk.CTkButton(
            self.left_frame,
            text="Perbarui Data (Update)",
            fg_color="blue",
            hover_color="darkblue",
            width=250,
            height=40,
        )
        self.btn_update.pack(pady=10)

        self.btn_delete = ctk.CTkButton(
            self.left_frame,
            text="Hapus Data (Delete)",
            fg_color="red",
            hover_color="darkred",
            width=250,
            height=40,
        )
        self.btn_delete.pack(pady=10)

        # Frame Kanan (Tabel & Identitas User)
        self.right_frame = ctk.CTkFrame(self)
        self.right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Header Identitas (Pojok Kanan Atas)
        header_text = f"{self.nama_user}\n{self.nim}"
        self.lbl_identitas = ctk.CTkLabel(
            self.right_frame,
            text=header_text,
            font=("Arial", 11, "bold"),
            anchor="e",
            justify="right",
        )
        self.lbl_identitas.pack(side="top", fill="x", padx=15, pady=5)

        ctk.CTkLabel(
            self.right_frame, text="Daftar Koleksi Buku", font=("Arial", 16, "bold")
        ).pack(anchor="w", padx=15, pady=5)

        # Treeview Tabel Buku
        self.tree = ttk.Treeview(
            self.right_frame,
            columns=("ID", "Judul", "Penulis", "Tahun"),
            show="headings",
        )
        self.tree.heading("ID", text="ID")
        self.tree.heading("Judul", text="Judul Buku")
        self.tree.heading("Penulis", text="Penulis")
        self.tree.heading("Tahun", text="Tahun")

        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Judul", width=200, anchor="w")
        self.tree.column("Penulis", width=150, anchor="w")
        self.tree.column("Tahun", width=80, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=15, pady=10)

    def load_data_buku(self):
        """Mengambil data dari MySQL dan memasukkannya ke dalam tabel Treeview."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        buku_list = self.model_buku.get_all_buku()
        if buku_list:
            for buku in buku_list:
                # Menangani format dictionary maupun tuple dari query database
                if isinstance(buku, dict):
                    self.tree.insert(
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
                    self.tree.insert("", "end", values=buku)


if __name__ == "__main__":
    app = AnggotaView()
    app.mainloop()
