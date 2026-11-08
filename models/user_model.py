
import hashlib
from config.database import Database


class UserModel:

    def __init__(self):
        self.db = Database()

        try:
            self.conn = self.db.get_connection()
        except ConnectionError as e:
            self.conn = None
            self.error = str(e)
        else:
            self.error = None

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(
            password.encode("utf-8")
        ).hexdigest()

    def autentikasi(self, username, password):

        if not self.conn:
            raise ConnectionError(
                self.error or "Database tidak terhubung."
            )

        cursor = self.conn.cursor(dictionary=True)

        try:
            hashed_pw = self.hash_password(password)

            query = """
                SELECT * FROM users
                WHERE username = %s AND password = %s
            """

            cursor.execute(query, (username, hashed_pw))

            return cursor.fetchone()

        finally:
            cursor.close()
