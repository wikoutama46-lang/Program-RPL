
from unittest.mock import MagicMock, patch
from models.buku_model import BukuModel


@patch("config.database.Database.get_connection")
def test_create_buku_berhasil(mock_get_conn):
    model = BukuModel()

    model.conn = MagicMock()
    mock_cursor = MagicMock()
    model.conn.cursor.return_value = mock_cursor

    hasil = model.create_buku("Buku Testing", "Penulis QA", 2026)

    assert hasil is True
    mock_cursor.execute.assert_called_once()
    model.conn.commit.assert_called_once()


@patch("config.database.Database.get_connection")
def test_get_all_buku_berhasil(mock_get_conn):
    # 1. Inisialisasi model
    model = BukuModel()

    # 2. Mock koneksi database dan cursor
    model.conn = MagicMock()
    mock_cursor = MagicMock()
    model.conn.cursor.return_value = mock_cursor

    # 3. Buat data dummy yang akan dikembalikan oleh fetchall()
    data_dummy = [
        {'id_buku': 1, 'judul': 'Laut Bercerita', 'penulis': 'Leila S. Chudori', 'tahun_terbit': 2017},
        {'id_buku': 2, 'judul': 'Aroma Karsa', 'penulis': 'Dee Lestari', 'tahun_terbit': 2018}
    ]
    mock_cursor.fetchall.return_value = data_dummy

    # 4. Eksekusi fungsi
    hasil = model.get_all_buku()

    # 5. Verifikasi pengujian
    assert hasil == data_dummy
    assert len(hasil) == 2
    mock_cursor.execute.assert_called_once_with("SELECT * FROM buku")