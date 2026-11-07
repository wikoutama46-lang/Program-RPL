"""Halaman Daftar Data (GUI): tabel data satu modul, pencarian, dan tombol aksi."""
import customtkinter as ctk
from tkinter import ttk

from views import tema as t
from views.modul import MODUL, URUTAN, kunci_dari_judul


class DaftarView(ctk.CTkFrame):
    def __init__(self, master, on_ganti_modul=None):
        super().__init__(master, fg_color=t.LATAR)
        self._on_ganti_modul = on_ganti_modul
        self.modul = URUTAN[0]
        self._semua = []        # seluruh baris (list of dict) dari controller
        self._baris = {}        # {iid treeview: dict baris asli}

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.panel = t.panel(self)
        self.panel.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.panel.grid_columnconfigure(0, weight=1)
        self.panel.grid_rowconfigure(2, weight=1)

        # Baris judul + pilihan modul
        kepala = ctk.CTkFrame(self.panel, fg_color="transparent")
        kepala.grid(row=0, column=0, padx=15, pady=(15, 0), sticky="ew")
        kepala.grid_columnconfigure(0, weight=1)
        self.lbl_judul = t.judul(kepala, "Daftar Data")
        self.lbl_judul.grid(row=0, column=0, sticky="w")
        t.teks(kepala, "Modul:", sekunder=True).grid(row=0, column=1, padx=(0, 8))
        self.pilih_modul = t.menu_pilihan(
            kepala, [MODUL[k]["judul"] for k in URUTAN], command=self._modul_dipilih, width=140)
        self.pilih_modul.grid(row=0, column=2)

        # Pencarian
        self.entry_cari = t.entri(self.panel, "Cari data (ketik lalu hasil tersaring otomatis)")
        self.entry_cari.grid(row=1, column=0, padx=15, pady=10, sticky="ew")
        self.entry_cari.bind("<KeyRelease>", lambda _e: self._isi_tabel())

        # Tabel + scrollbar
        wadah = ctk.CTkFrame(self.panel, fg_color="transparent")
        wadah.grid(row=2, column=0, padx=15, sticky="nsew")
        wadah.grid_columnconfigure(0, weight=1)
        wadah.grid_rowconfigure(0, weight=1)
        self.tabel = ttk.Treeview(wadah, show="headings", selectmode="browse", height=8)
        sb_y = ttk.Scrollbar(wadah, orient="vertical", command=self.tabel.yview)
        sb_x = ttk.Scrollbar(wadah, orient="horizontal", command=self.tabel.xview)
        self.tabel.configure(yscrollcommand=sb_y.set, xscrollcommand=sb_x.set)
        self.tabel.grid(row=0, column=0, sticky="nsew")
        sb_y.grid(row=0, column=1, sticky="ns")
        sb_x.grid(row=1, column=0, sticky="ew")

        # Tombol aksi + total
        bar = ctk.CTkFrame(self.panel, fg_color="transparent")
        bar.grid(row=3, column=0, padx=15, pady=(10, 15), sticky="ew")
        self.btn_tambah = t.tombol(bar, "Tambah", "utama", width=100)
        self.btn_ubah = t.tombol(bar, "Ubah", "kedua", width=100)
        self.btn_hapus = t.tombol(bar, "Hapus", "bahaya", width=100)
        self.btn_muat = t.tombol(bar, "Muat Ulang", "garis", width=110)
        for tb in (self.btn_tambah, self.btn_ubah, self.btn_hapus, self.btn_muat):
            tb.pack(side="left", padx=(0, 8))
        self.lbl_total = t.teks(bar, "Total: 0 data", sekunder=True)
        self.lbl_total.pack(side="right")

        self.atur_modul(self.modul)

    # ---------- internal ----------
    def _modul_dipilih(self, judul_modul):
        kunci = kunci_dari_judul(judul_modul)
        self.atur_modul(kunci)
        if self._on_ganti_modul:
            self._on_ganti_modul(kunci)

    def _isi_tabel(self):
        """Tampilkan _semua ke tabel, disaring oleh kata kunci pencarian (hanya tampilan)."""
        kata = self.entry_cari.get().strip().lower()
        kolom = MODUL[self.modul]["kolom"]
        self.tabel.delete(*self.tabel.get_children())
        self._baris = {}
        for i, d in enumerate(self._semua):
            nilai = ["-" if d.get(k) in (None, "") else str(d.get(k)) for k, _h, _w in kolom]
            if kata and not any(kata in v.lower() for v in nilai):
                continue
            iid = str(i)
            self._baris[iid] = d
            self.tabel.insert("", "end", iid=iid, values=nilai)
        self.lbl_total.configure(text=f"Total: {len(self._baris)} data")

    # ===== Method bantu untuk Controller (tanpa logika bisnis) =====
    def atur_modul(self, kunci):
        """Ganti modul: kolom tabel disesuaikan, data dikosongkan sampai Controller mengisi."""
        self.modul = kunci
        m = MODUL[kunci]
        self.pilih_modul.set(m["judul"])
        self.lbl_judul.configure(text=f"Daftar Data {m['judul']}")
        self.tabel.configure(columns=[k for k, _h, _w in m["kolom"]])
        for k, h, w in m["kolom"]:
            self.tabel.heading(k, text=h)
            self.tabel.column(k, width=w, minwidth=40,
                              anchor="center" if k.startswith("id_") or w <= 90 else "w")
        self.entry_cari.delete(0, "end")
        self.tampilkan_data([])

    def tampilkan_data(self, daftar):
        """Menampilkan list of dict (hasil model.get_all()) ke tabel."""
        self._semua = list(daftar or [])
        self._isi_tabel()

    def data_terpilih(self):
        """Dict baris yang dipilih di tabel, atau None."""
        pilihan = self.tabel.selection()
        return self._baris.get(pilihan[0]) if pilihan else None

    def id_terpilih(self):
        data = self.data_terpilih()
        return data.get(MODUL[self.modul]["id"]) if data else None

    def tampilkan_pesan(self, teks, error=False):
        (t.pesan_error if error else t.pesan_info)(teks)

    def konfirmasi_hapus(self):
        return t.konfirmasi("Yakin ingin menghapus data yang dipilih?")