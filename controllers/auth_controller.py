
import tkinter.messagebox as messagebox
from models.user_model import UserModel
from views.login_view import LoginView


class AuthController:

    def __init__(self):
        self.model = UserModel()
        self.view = LoginView()
        self.view.btn_login.configure(
            command=self.proses_login
        )

    def proses_login(self):
        username = self.view.entry_username.get().strip()
        password = self.view.entry_password.get()

        if not username or not password:
            messagebox.showwarning(
                "Peringatan",
                "Username dan Password wajib diisi!"
            )
            return

        try:
            user = self.model.autentikasi(
                username, password
            )

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                f"Gagal memproses login:\n{e}"
            )
            return

        if user:
            messagebox.showinfo(
                "Login Berhasil",
                f"Selamat datang, {user['username']} "
                f"({user['role']})!"
            )

            self.view.withdraw()

            try:
                from controllers.buku_controller import BukuController

                role_pengguna = user.get("role", "anggota")
                self.app_utama = BukuController(
                    user_role=role_pengguna
                )

                self.view.destroy()
                self.app_utama.run()

            except Exception as e:
                messagebox.showerror(
                    "Application Error",
                    str(e)
                )
                self.view.deiconify()

        else:
            messagebox.showerror(
                "Login Gagal",
                "Username atau Password salah!"
            )

    def run(self):
        self.view.mainloop()
