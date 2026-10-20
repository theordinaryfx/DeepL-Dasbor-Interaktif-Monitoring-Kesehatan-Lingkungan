# 🌿 Dasbor Interaktif Monitoring Kesehatan Lingkungan
### Perancangan Berbasis User-Centered Design (UCD) dan Mantra Shneiderman

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)
![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Charts-3F4F75)
![HCI](https://img.shields.io/badge/HCI-UCD%20%7C%20WCAG-green)

Proyek portofolio **Interaksi Manusia dan Komputer (IMK)** dan **Visualisasi Data**. Dasbor web ini menampilkan data kualitas udara dan kondisi lingkungan kota dengan antarmuka yang **ringan secara kognitif**, **bersih dari chartjunk**, dan **mengikuti alur eksplorasi Mantra Shneiderman**.

> ⚠️ **Catatan:** Data adalah **data dummy** untuk demonstrasi. Ambang kategori AQI disederhanakan.

---

## 📑 Daftar Isi
1. [Pendekatan User-Centered Design (UCD)](#1--pendekatan-user-centered-design-ucd)
2. [Penerapan Prinsip IMK & Persepsi Visual](#2--penerapan-prinsip-imk--persepsi-visual)
3. [Usability Evaluation & Accessibility](#3--usability-evaluation--accessibility)
4. [Cara Menjalankan Aplikasi](#4--cara-menjalankan-aplikasi)
5. [Struktur Repositori](#5--struktur-repositori)

---

## 1. 👤 Pendekatan User-Centered Design (UCD)

### User Persona
> **Robi, 27 tahun, Analis Lingkungan** di instansi pengelola lingkungan kota *(persona ilustratif)*.

| Aspek | Uraian |
|---|---|
| **Tujuan** | Mengetahui cepat stasiun mana yang kualitas udaranya memburuk dan menyiapkan laporan harian |
| **Kebutuhan** | Gambaran umum sekilas, perbandingan antarstasiun, angka rinci untuk dikutip ke laporan |
| **Kendala** | Waktu terbatas, data banyak, grafik penuh dekorasi menyulitkan pembacaan |
| **Kemampuan teknis** | Memahami AQI dan istilah lingkungan, bukan programmer |

### Skenario Penggunaan
1. Pagi hari, Rina membuka dasbor dan langsung melihat **KPI ringkasan**: rata-rata AQI dan jumlah stasiun Tidak Sehat.
2. Ia mencurigai satu kawasan, lalu **menyaring** rentang tanggal minggu ini dan stasiun terkait di sidebar.
3. Ia membaca **grafik tren** dan **perbandingan stasiun**, lalu mengarahkan kursor ke titik yang melonjak untuk melihat **AQI, CO₂, suhu, dan kelembapan** saat itu.
4. Ia membuka **tabel rinci** dan **mengunduh CSV** untuk lampiran laporan.

### Kebutuhan → Keputusan Desain
| Kebutuhan pengguna | Keputusan desain |
|---|---|
| "Saya ingin tahu kondisi umum dulu" | KPI ringkasan di bagian paling atas |
| "Saya hanya peduli stasiun/hari tertentu" | Filter tanggal dan stasiun di sidebar |
| "Saya butuh angka pasti untuk laporan" | Tooltip hover, tabel rinci, dan tombol unduh |
| "Saya tidak ingin dibanjiri informasi" | Detail disembunyikan sampai diminta (hover/expander) |

> 🔎 Persona di atas adalah hipotesis awal. Pada praktik UCD sesungguhnya, persona disusun dari **wawancara dan observasi pengguna nyata**.

---

## 2. 🧠 Penerapan Prinsip IMK & Persepsi Visual

### 2.1 Pengelolaan Beban Kognitif
Beban kognitif dibagi menjadi *intrinsic* (kompleksitas data itu sendiri), *extraneous* (akibat cara penyajian), dan *germane* (usaha membangun pemahaman). Antarmuka ini **meminimalkan extraneous load**:

| Teknik | Penerapan |
|---|---|
| **Satu tujuan per komponen** | Setiap grafik menjawab satu pertanyaan (tren vs perbandingan) |
| **Pengungkapan bertahap** | Detail baru muncul saat hover atau membuka expander |
| **Label langsung** | Nilai dan status tertulis pada batang, tanpa perlu mencocokkan legenda |
| **Nilai bawaan yang masuk akal** | Semua stasiun dan seluruh periode terpilih saat dasbor dibuka |
| **Umpan balik jelas** | Pesan peringatan bila filter menghasilkan data kosong |
| **Konsistensi** | Warna status dan urutan kategori sama di seluruh komponen |

### 2.2 Atribut Preatentif & Prinsip Gestalt
**Atribut preatentif** diproses otak dalam hitungan milidetik tanpa fokus sadar. Dasbor memakai:
- **Warna (hue)**: hijau-teal, oker, dan merah tua langsung menandai status Baik, Sedang, dan Tidak Sehat.
- **Posisi & panjang**: batang diurutkan sehingga stasiun terburuk selalu berada di atas.
- **Bentuk (marker)**: simbol berbeda per stasiun pada grafik tren.

**Prinsip Gestalt:**
| Prinsip | Penerapan |
|---|---|
| **Proximity** | Filter dikelompokkan di sidebar; KPI berdampingan; judul dekat grafiknya |
| **Enclosure** | KPI dan setiap grafik dibingkai kontainer berborder sehingga terbaca sebagai satu kelompok |
| **Similarity** | Warna status konsisten untuk makna yang sama |
| **Continuity** | Garis tren menuntun mata mengikuti perubahan antarwaktu |

### 2.3 Eliminasi Chartjunk (Data-Ink Ratio Tufte)

> **Data-ink ratio** = tinta yang merepresentasikan data ÷ total tinta pada grafik. Semakin tinggi, semakin jujur dan bersih grafiknya.

| Elemen | Keputusan |
|---|---|
| Garis kisi (grid) | ❌ Dihapus |
| Efek 3D, bayangan, gradien | ❌ Tidak dipakai |
| Latar bertekstur / dekorasi | ❌ Tidak dipakai, latar putih polos |
| Toolbar bawaan grafik | ❌ Disembunyikan |
| Sumbu nilai pada bar chart | ❌ Diganti label langsung |
| Garis acuan ambang AQI | ✅ Dipertahankan (membawa informasi) |
| Sumbu dasar dan label | ✅ Dipertahankan, tipis dan jelas |

Grafik **jujur**: sumbu bar chart dimulai dari nol, sehingga panjang batang proporsional dengan nilai.

### 2.4 Mantra Interaksi Shneiderman

```
OVERVIEW FIRST  ──►  ZOOM AND FILTER  ──►  DETAILS-ON-DEMAND
 (KPI ringkasan)      (sidebar tanggal       (tooltip hover, expander
                       & stasiun, zoom        tabel rinci, unduh CSV)
                       grafik)
```

| Tahap | Implementasi di dasbor |
|---|---|
| **Overview first** | Empat KPI: rata-rata AQI, jumlah stasiun Tidak Sehat, AQI puncak, rata-rata CO₂ |
| **Zoom and filter** | Rentang tanggal dan multiselect stasiun; zoom drag pada grafik tren |
| **Details-on-demand** | Tooltip (AQI, status, CO₂, suhu, kelembapan), tabel rinci, dan unduhan CSV |

---

## 3. ✅ Usability Evaluation & Accessibility

### 3.1 Usability Testing dengan Think-Aloud Protocol
Partisipan diminta **mengucapkan pikirannya** saat mengerjakan tugas, sehingga hambatan dan kebingungan terdeteksi.

**Rencana pengujian:**
| Item | Rencana |
|---|---|
| **Partisipan** | 5 orang per putaran (mewakili persona analis atau pengguna sejenis) |
| **Tugas 1** | Sebutkan stasiun dengan kondisi terburuk saat ini |
| **Tugas 2** | Cari AQI dan kadar CO₂ stasiun X pada tanggal tertentu |
| **Tugas 3** | Tampilkan hanya 2 stasiun pada 3 hari terakhir |
| **Tugas 4** | Unduh data hasil filter |
| **Metrik** | Task success rate, waktu penyelesaian, jumlah kesalahan, skor **SUS** (System Usability Scale), kutipan kualitatif |
| **Prosedur** | Briefing → tugas sambil berpikir keras → wawancara singkat → SUS |
| **Iterasi** | Temuan diprioritaskan (tingkat keparahan), desain diperbaiki, lalu diuji ulang |

Pelengkap: **Heuristic Evaluation** dengan 10 heuristik Nielsen (visibilitas status sistem, konsistensi, pencegahan kesalahan, dan lainnya).

### 3.2 Aksesibilitas (WCAG)
| Kriteria WCAG | Penerapan |
|---|---|
| **1.4.3 Kontras teks (≥ 4,5:1)** | Warna status gelap di atas latar putih; teks utama hampir hitam |
| **1.4.11 Kontras non-teks (≥ 3:1)** | Batang, garis, dan marker berkontras memadai terhadap latar |
| **1.4.1 Penggunaan warna** | Warna **bukan satu-satunya penanda**: ada label teks status dan simbol marker berbeda |
| **Ukuran teks** | Font grafik 14 px ke atas |
| **Alternatif non-visual** | Tabel data rinci menyediakan data yang sama dalam bentuk teks |
| **Keyboard** | Widget bawaan Streamlit dapat dioperasikan dengan keyboard |

**Perkiraan rasio kontras terhadap putih** (verifikasi dengan WebAIM Contrast Checker atau Lighthouse):

| Warna | Kode | Perkiraan rasio |
|---|---|---|
| Baik | `#00695C` | ≈ 6,6 : 1 |
| Sedang | `#A25E00` | ≈ 5,1 : 1 |
| Tidak Sehat | `#C62828` | ≈ 5,6 : 1 |

> ℹ️ Kepatuhan WCAG penuh memerlukan audit menyeluruh (termasuk pembaca layar). Proyek ini menerapkan praktik kunci dan menjadikannya bagian dari rencana evaluasi.

---

## 4. ▶️ Cara Menjalankan Aplikasi

```bash
# 1. Clone repositori
git clone https://github.com/<username>/<nama-repositori>.git
cd <nama-repositori>

# 2. (Opsional) Buat virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Instal dependensi
pip install -r requirements.txt

# 4. Jalankan dasbor
streamlit run dashboard_app.py
```

Aplikasi terbuka di `http://localhost:8501`.

**Opsional:** agar tampilan konsisten (latar terang) di semua perangkat, buat file `.streamlit/config.toml`:

```toml
[theme]
base = "light"
```

📸 *Tambahkan tangkapan layar dasbor di sini:* `![Dasbor](images/dasbor.png)`

---

## 5. 📁 Struktur Repositori

```
├── data_pemantauan_lingkungan.csv   # Data dummy (25 baris)
├── dashboard_app.py                 # Aplikasi dasbor Streamlit + Plotly
├── requirements.txt                 # Dependensi Python
├── .streamlit/config.toml           # (opsional) tema terang
└── README.md                        # Dokumentasi proyek
```

**Satuan data:** CO₂ dalam ppm, suhu dalam °C, kelembapan dalam %.

---

## 🚀 Pengembangan Lanjutan
- Tambahkan peta sebaran stasiun (geospasial).
- Mode tema gelap dengan palet yang tetap lolos kontras.
- Notifikasi ambang kritis dan ekspor laporan PDF.
- Jalankan putaran usability testing nyata dan dokumentasikan hasilnya.
