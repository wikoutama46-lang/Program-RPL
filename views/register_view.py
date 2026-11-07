import customtkinter as ctk

class RegisterView(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Daftar Akun - Sistem Perpustakaan")
        self.geometry("360x470")
        self.resizable(False, False)

        # Jendela register tampil di atas jendela Login dan bersifat modal
        self.transient(master)
        self.after(150, self.grab_set)

        self.frame = ctk.CTkFrame(self)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        ctk.CTkLabel(self.frame, text="DAFTAR AKUN", font=("Arial", 18, "bold")).pack(pady=(20, 15))

        self.entry_username = ctk.CTkEntry(self.frame, placeholder_text="Username")
        self.entry_username.pack(pady=8, padx=20, fill="x")

        self.entry_password = ctk.CTkEntry(self.frame, placeholder_text="Password", show="*")
        self.entry_password.pack(pady=8, padx=20, fill="x")

        self.entry_konfirmasi = ctk.CTkEntry(self.frame, placeholder_text="Konfirmasi Password", show="*")
        self.entry_konfirmasi.pack(pady=8, padx=20, fill="x")

        ctk.CTkLabel(self.frame, text="Role").pack(pady=(8, 0), padx=20, anchor="w")
        self.opt_role = ctk.CTkOptionMenu(self.frame, values=["anggota", "admin"])
        self.opt_role.set("anggota")
        self.opt_role.pack(pady=(0, 8), padx=20, fill="x")

        self.btn_daftar = ctk.CTkButton(self.frame, text="Daftar", fg_color="green")
        self.btn_daftar.pack(pady=(15, 5), padx=20, fill="x")

        self.btn_batal = ctk.CTkButton(self.frame, text="Batal", fg_color="gray", command=self.destroy)
        self.btn_batal.pack(pady=(0, 15), padx=20, fill="x")
