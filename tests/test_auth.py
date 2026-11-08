from unittest.mock import MagicMock, patch
from models.user_model import UserModel


def test_hash_password_konsisten():
    password_asli = "admin123"
    hash_1 = UserModel.hash_password(password_asli)
    hash_2 = UserModel.hash_password(password_asli)

    # Memastikan hasil hash tidak sama dengan plaintext asli
    assert hash_1 != password_asli
    assert hash_1 == hash_2
    assert len(hash_1) == 64  # Panjang karakter standar SHA-256


@patch("config.database.Database.get_connection")
def test_autentikasi_pengguna_berhasil(mock_get_conn):
    # Mock koneksi database agar tidak memicu error koneksi MySQL di server CI
    mock_conn = MagicMock()
    mock_get_conn.return_value = mock_conn

    model = UserModel()
    mock_cursor = MagicMock()

    # Simulasi kembalian data dari database ketika username & password cocok
    mock_cursor.fetchone.return_value = {
        "id_user": 1,
        "username": "petugas",
        "role": "admin"
    }
    model.conn.cursor.return_value = mock_cursor

    hasil = model.autentikasi("petugas", "admin123")

    assert hasil is not None
    assert hasil["username"] == "petugas"
    assert hasil["role"] == "admin"