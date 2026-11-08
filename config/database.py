import mysql.connector
from mysql.connector import Error


class Database:

    def __init__(self):
        self.host = "localhost"
        self.port = 3306
        self.db_name = "perpustakaan"
        self.username = "root"
        self.password = ""
        self.conn = None

    def get_connection(self):
        """Membuka koneksi baru ke database MySQL."""
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                port=self.port,
                database=self.db_name,
                user=self.username,
                password=self.password,
                connection_timeout=5,
                use_pure=True,  # pakai implementasi Python murni (tanpa DLL C)
            )

            if self.conn.is_connected():
                return self.conn

        except Error as e:
            print(f"Koneksi MySQL Gagal: {e}")
            raise ConnectionError(f"Gagal menghubungkan database: {e}")

        return None

    def close_connection(self):
        """Menutup koneksi jika masih terbuka."""
        if self.conn is not None and self.conn.is_connected():
            self.conn.close()
            self.conn = None