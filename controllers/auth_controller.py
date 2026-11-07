import tkinter.messagebox as messagebox
from models.user_model import UserModel
from views.login_view import LoginView
from views.register_view import RegisterView
from controllers.buku_controller import BukuController

class AuthController:
    def __init__(self):
        self.model = UserModel()
        self.view = LoginView()
        self.view.btn_login.configure(command=self.proses_login)
        self.view.btn_register.configure(command=self.buka_register)
        self.register_view = None

    def proses_login(self):
        username = self.view.entry_username.get()
        password = self.view.entry_password.get()

        if not username or not password:
            messagebox.showwarning("Peringatan", "Username dan Password wajib diisi!")
            return

        user = self.model.autentikasi(username, password)

        if user:
            messagebox.showinfo("Login Berhasil", f"Selamat datang, {user['username']} ({user['role']})!")
            # Tutup jendela Login
            self.view.destroy()

            # Buka jendela Utama Perpustakaan dengan mengirimkan role pengguna
            app_utama = BukuController(user_role=user['role'])
            app_utama.run()
        else:
            messagebox.showerror("Login Gagal", "Username atau Password salah!")

    def buka_register(self):
        # Cegah jendela register terbuka ganda
        if self.register_view is not None and self.register_view.winfo_exists():
            self.register_view.focus()
            return
        self.register_view = RegisterView(self.view)
        self.register_view.btn_daftar.configure(command=self.proses_register)

    def proses_register(self):
        v = self.register_view
        username = v.entry_username.get().strip()
        password = v.entry_password.get()
        konfirmasi = v.entry_konfirmasi.get()
        role = v.opt_role.get()

        if not username or not password or not konfirmasi:
            messagebox.showwarning("Peringatan", "Semua kolom wajib diisi!", parent=v)
            return

        if len(password) < 6:
            messagebox.showwarning("Peringatan", "Password minimal 6 karakter!", parent=v)
            return

        if password != konfirmasi:
            messagebox.showwarning("Peringatan", "Konfirmasi password tidak sama!", parent=v)
            return

        if self.model.register_user(username, password, role):
            messagebox.showinfo("Berhasil", f"Akun '{username}' ({role}) berhasil dibuat. Silakan login.", parent=v)
            v.destroy()
            # Isi otomatis username pada form Login
            self.view.entry_username.delete(0, "end")
            self.view.entry_username.insert(0, username)
            self.view.entry_password.focus()
        else:
            messagebox.showerror("Gagal", "Pendaftaran gagal. Username mungkin sudah digunakan.", parent=v)

    def run(self):
        self.view.mainloop()