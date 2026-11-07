from unittest.mock import MagicMock
from models.buku_model import BukuModel


def test_create_buku_berhasil():
    # Menginisialisasi Model
    model = BukuModel()

    # Memanipulasi (Mock) koneksi database agar tidak mengotori data asli
    model.conn = MagicMock()
    mock_cursor = MagicMock()
    model.conn.cursor.return_value = mock_cursor

    # Melakukan eksekusi fungsi
    hasil = model.create_buku("Buku Testing", "Penulis QA", 2026)

    # Memverifikasi apakah fungsi mengembalikan nilai True
    assert hasil is True

    # Memverifikasi apakah perintah execute benar-benar dipanggil
    mock_cursor.execute.assert_called_once()

    # Memverifikasi apakah perintah commit (simpan) dipanggil
    model.conn.commit.assert_called_once()

def test_get_all_buku_berhasil():
    # Menginisialisasi Model
    model = BukuModel()

    # Memanipulasi (Mock) koneksi database agar tidak membaca data asli
    data_palsu = [
        {"id_buku": 1, "judul": "Buku A", "penulis": "Penulis A", "tahun_terbit": 2020},
        {"id_buku": 2, "judul": "Buku B", "penulis": "Penulis B", "tahun_terbit": 2021},
    ]
    model.conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = data_palsu
    model.conn.cursor.return_value = mock_cursor

    # Melakukan eksekusi fungsi
    hasil = model.get_all_buku()

    # Memverifikasi apakah hasilnya sama dengan data dari cursor
    assert hasil == data_palsu
    assert len(hasil) == 2

    # Memverifikasi apakah query SELECT dijalankan lalu cursor ditutup
    mock_cursor.execute.assert_called_once()
    assert "SELECT" in mock_cursor.execute.call_args[0][0]
    mock_cursor.close.assert_called_once()
