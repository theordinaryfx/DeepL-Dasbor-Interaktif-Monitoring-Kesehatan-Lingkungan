"""
Dasbor Interaktif Monitoring Kesehatan Lingkungan
=================================================
Rancangan berbasis User-Centered Design (UCD) dan Mantra Shneiderman:
  1. OVERVIEW FIRST    -> KPI ringkasan makro di bagian paling atas.
  2. ZOOM AND FILTER   -> Filter rentang tanggal & stasiun di sidebar.
  3. DETAILS-ON-DEMAND -> Tooltip hover pada grafik + tabel rincian (expander).

Prinsip visualisasi:
  - Kurangi beban kognitif ekstranus: satu tujuan per komponen, label langsung.
  - Warna status berkontras tinggi (rasio >= 4,5:1 terhadap putih) dan tidak
    menjadi satu-satunya penanda (selalu ada label teks / simbol marker).
  - Bebas chartjunk: tanpa grid, tanpa 3D, tanpa dekorasi (rasio data-ink tinggi).

Jalankan: streamlit run dashboard_app.py
"""

# ---------------------------------------------------------------
# 1. IMPORT LIBRARY
# ---------------------------------------------------------------
import pandas as pd
import plotly.express as px
import streamlit as st

# ---------------------------------------------------------------
# 2. KONFIGURASI HALAMAN & KONSTANTA
# ---------------------------------------------------------------
st.set_page_config(
    page_title="Dasbor Kesehatan Lingkungan",
    page_icon="🌿",
    layout="wide",
)

FILE_DATA = "data_pemantauan_lingkungan.csv"
KOLOM_AQI = "Indeks_Kualitas_Udara_AQI"

# Ambang kategori (disederhanakan; sesuaikan dengan standar ISPU yang berlaku)
BATAS_BAIK = 50
BATAS_TIDAK_SEHAT = 100

URUTAN_STATUS = ["Baik", "Sedang", "Tidak Sehat"]

# Warna STATUS: dipilih gelap agar kontras terhadap latar putih >= 4,5:1
# (perkiraan: hijau-teal ~6,6:1 | oker ~5,1:1 | merah ~5,6:1).
WARNA_STATUS = {
    "Baik": "#00695C",
    "Sedang": "#A25E00",
    "Tidak Sehat": "#C62828",
}

# Warna STASIUN (garis tren): sengaja netral/biru-ungu agar tidak bentrok
# dengan makna warna status (hijau/oker/merah). Dipadukan dengan simbol marker
# berbeda sehingga tetap terbedakan tanpa bergantung pada warna saja.
PALET_STASIUN = ["#0B3C5D", "#6A3D9A", "#4D4D4D", "#0072B2", "#B5179E"]


def kategori_aqi(nilai: float) -> str:
    """Tentukan kategori dari nilai AQI."""
    if nilai <= BATAS_BAIK:
        return "Baik"
    if nilai <= BATAS_TIDAK_SEHAT:
        return "Sedang"
    return "Tidak Sehat"


# ---------------------------------------------------------------
# 3. MEMUAT DATA
# ---------------------------------------------------------------
@st.cache_data
def muat_data(path: str) -> pd.DataFrame:
    """Muat CSV sekali saja (di-cache) agar interaksi terasa cepat."""
    df = pd.read_csv(path, parse_dates=["Tanggal_Waktu"])
    return df.sort_values("Tanggal_Waktu").reset_index(drop=True)


def rapikan_grafik(fig):
    """Terapkan gaya minimalis: rasio data-ink tinggi, tanpa chartjunk."""
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Arial, sans-serif", size=14, color="#1A1A1A"),
        margin=dict(l=10, r=10, t=10, b=10),
        hoverlabel=dict(bgcolor="white", font_size=14),
        legend=dict(title_text="", orientation="h", yanchor="top", y=-0.2),
    )
    # Tanpa garis kisi; hanya garis sumbu tipis sebagai acuan
    fig.update_xaxes(showgrid=False, showline=True, linecolor="#595959", title_text="")
    fig.update_yaxes(showgrid=False, showline=True, linecolor="#595959")
    return fig


df = muat_data(FILE_DATA)

# ---------------------------------------------------------------
# 4. JUDUL & PETUNJUK SINGKAT
# ---------------------------------------------------------------
st.title("🌿 Dasbor Monitoring Kesehatan Lingkungan")
st.caption(
    "Mulai dari ringkasan di bawah, persempit data lewat filter di sisi kiri, "
    "lalu arahkan kursor ke grafik untuk melihat angka rinci."
)

# ---------------------------------------------------------------
# 5. ZOOM AND FILTER: KONTROL SIDEBAR
# ---------------------------------------------------------------
with st.sidebar:
    st.header("Filter Data")

    tgl_min = df["Tanggal_Waktu"].dt.date.min()
    tgl_maks = df["Tanggal_Waktu"].dt.date.max()
    rentang = st.date_input(
        "Rentang tanggal",
        value=(tgl_min, tgl_maks),
        min_value=tgl_min,
        max_value=tgl_maks,
    )

    semua_stasiun = sorted(df["Lokasi_Stasiun"].unique())
    stasiun_dipilih = st.multiselect(
        "Stasiun pemantauan", options=semua_stasiun, default=semua_stasiun
    )
    st.caption(
        f"Ambang AQI: Baik ≤ {BATAS_BAIK} | Sedang {BATAS_BAIK + 1}–{BATAS_TIDAK_SEHAT} "
        f"| Tidak Sehat > {BATAS_TIDAK_SEHAT}"
    )

# date_input dapat mengembalikan 1 tanggal saat pengguna baru memilih awal rentang
if isinstance(rentang, (tuple, list)):
    tgl_awal = rentang[0]
    tgl_akhir = rentang[1] if len(rentang) > 1 else rentang[0]
else:
    tgl_awal = tgl_akhir = rentang

tanggal = df["Tanggal_Waktu"].dt.date
dff = df[
    tanggal.between(tgl_awal, tgl_akhir) & df["Lokasi_Stasiun"].isin(stasiun_dipilih)
].copy()

# Keadaan kosong: beri umpan balik jelas, bukan layar kosong
if dff.empty:
    st.warning("Tidak ada data untuk filter ini. Ubah rentang tanggal atau pilih stasiun.")
    st.stop()

# ---------------------------------------------------------------
# 6. OVERVIEW FIRST: KPI RINGKASAN MAKRO
# ---------------------------------------------------------------
st.subheader("1 · Ringkasan")

rata_aqi = dff[KOLOM_AQI].mean()
terbaru = dff.sort_values("Tanggal_Waktu").groupby("Lokasi_Stasiun").tail(1)
jml_tidak_sehat = int((terbaru["Status_Kategori"] == "Tidak Sehat").sum())
baris_puncak = dff.loc[dff[KOLOM_AQI].idxmax()]
rata_co2 = dff["Konsentrasi_CO2"].mean()

# Enclosure (Gestalt): KPI dikelompokkan dalam satu bingkai
with st.container(border=True):
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Rata-rata AQI", f"{rata_aqi:.1f}",
              help="Rata-rata AQI seluruh pengamatan sesuai filter.")
    k1.caption(f"Kategori: **{kategori_aqi(rata_aqi)}**")

    k2.metric("Stasiun Tidak Sehat", f"{jml_tidak_sehat} dari {len(terbaru)}",
              help="Berdasarkan pembacaan terbaru tiap stasiun pada periode terpilih.")
    k2.caption("Pembacaan terbaru per stasiun")

    k3.metric("AQI Puncak", f"{baris_puncak[KOLOM_AQI]:.0f}",
              help="Nilai AQI tertinggi pada periode terpilih.")
    k3.caption(f"Di **{baris_puncak['Lokasi_Stasiun']}**")

    k4.metric("Rata-rata CO₂", f"{rata_co2:.0f} ppm")
    k4.caption("Seluruh pengamatan terfilter")

# ---------------------------------------------------------------
# 7. DETAILS-ON-DEMAND: GRAFIK INTERAKTIF
# ---------------------------------------------------------------
st.subheader("2 · Tren dan Perbandingan")
kol_tren, kol_bar = st.columns([3, 2])

# --- Grafik tren AQI (line chart) ---
with kol_tren:
    with st.container(border=True):
        st.markdown("**Tren AQI per stasiun**")
        fig_tren = px.line(
            dff,
            x="Tanggal_Waktu",
            y=KOLOM_AQI,
            color="Lokasi_Stasiun",
            symbol="Lokasi_Stasiun",     # simbol berbeda: tidak hanya andalkan warna
            markers=True,
            color_discrete_sequence=PALET_STASIUN,
            custom_data=["Status_Kategori", "Konsentrasi_CO2",
                         "Suhu_Lingkungan", "Kelembapan"],
        )
        # Tooltip rinci muncul saat kursor diarahkan ke titik data
        fig_tren.update_traces(
            line=dict(width=2.5),
            marker=dict(size=9),
            hovertemplate=(
                "<b>%{fullData.name}</b><br>"
                "%{x|%d-%m-%Y %H:%M}<br>"
                "AQI: <b>%{y}</b> (%{customdata[0]})<br>"
                "CO₂: %{customdata[1]} ppm<br>"
                "Suhu: %{customdata[2]} °C<br>"
                "Kelembapan: %{customdata[3]}%"
                "<extra></extra>"
            ),
        )
        # Garis acuan ambang: data-ink bermakna, bukan dekorasi
        for batas, teks in [(BATAS_BAIK, f"Batas Baik ({BATAS_BAIK})"),
                            (BATAS_TIDAK_SEHAT, f"Batas Tidak Sehat ({BATAS_TIDAK_SEHAT})")]:
            fig_tren.add_hline(
                y=batas, line_dash="dot", line_color="#767676", line_width=1,
                annotation_text=teks, annotation_position="top left",
                annotation_font=dict(size=12, color="#595959"),
            )
        fig_tren.update_yaxes(title_text="AQI")
        fig_tren.update_xaxes(tickformat="%d %b")
        rapikan_grafik(fig_tren)
        st.plotly_chart(fig_tren, theme=None, config={"displayModeBar": False})
        st.caption("Seret untuk memperbesar area; klik dua kali untuk mengembalikan tampilan.")

# --- Grafik perbandingan stasiun (bar chart) ---
ringkas = dff.groupby("Lokasi_Stasiun").agg(
    Rata2_AQI=(KOLOM_AQI, "mean"),
    Maks_AQI=(KOLOM_AQI, "max"),
    Rata2_CO2=("Konsentrasi_CO2", "mean"),
    Pembacaan_Tidak_Sehat=("Status_Kategori", lambda s: int((s == "Tidak Sehat").sum())),
    Jumlah_Pembacaan=("Status_Kategori", "count"),
).reset_index()
ringkas["Status"] = ringkas["Rata2_AQI"].apply(kategori_aqi)
# Label langsung pada batang (angka + status): tidak perlu sumbu/legenda untuk membaca
ringkas["Label"] = ringkas["Rata2_AQI"].round(0).astype(int).astype(str) + " · " + ringkas["Status"]
ringkas = ringkas.sort_values("Rata2_AQI")  # terendah di bawah, tertinggi di atas

with kol_bar:
    with st.container(border=True):
        st.markdown("**Rata-rata AQI per stasiun**")
        fig_bar = px.bar(
            ringkas,
            x="Rata2_AQI",
            y="Lokasi_Stasiun",
            orientation="h",
            color="Status",
            color_discrete_map=WARNA_STATUS,
            category_orders={"Status": URUTAN_STATUS,
                             "Lokasi_Stasiun": list(ringkas["Lokasi_Stasiun"])},
            text="Label",
            custom_data=["Maks_AQI", "Rata2_CO2", "Pembacaan_Tidak_Sehat", "Jumlah_Pembacaan"],
        )
        fig_bar.update_traces(
            textposition="outside",
            cliponaxis=False,
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Rata-rata AQI: <b>%{x:.1f}</b><br>"
                "AQI maksimum: %{customdata[0]:.0f}<br>"
                "Rata-rata CO₂: %{customdata[1]:.0f} ppm<br>"
                "Pembacaan Tidak Sehat: %{customdata[2]} dari %{customdata[3]}"
                "<extra></extra>"
            ),
        )
        rapikan_grafik(fig_bar)
        # Sumbu x disembunyikan karena nilai sudah dilabel langsung (data-ink ratio)
        fig_bar.update_xaxes(visible=False, range=[0, ringkas["Rata2_AQI"].max() * 1.45])
        fig_bar.update_yaxes(title_text="")
        st.plotly_chart(fig_bar, theme=None, config={"displayModeBar": False})

        teratas = ringkas.iloc[-1]
        st.caption(f"Rata-rata tertinggi: **{teratas['Lokasi_Stasiun']}** "
                   f"({teratas['Rata2_AQI']:.1f}, {teratas['Status']}).")

# ---------------------------------------------------------------
# 8. DETAILS-ON-DEMAND: TABEL RINCI (DISEMBUNYIKAN SECARA DEFAULT)
# ---------------------------------------------------------------
st.subheader("3 · Rincian Data")
with st.expander("Lihat tabel data terfilter"):
    tabel = dff.rename(columns={
        "Tanggal_Waktu": "Tanggal & Waktu",
        "Lokasi_Stasiun": "Stasiun",
        KOLOM_AQI: "AQI",
        "Konsentrasi_CO2": "CO₂ (ppm)",
        "Suhu_Lingkungan": "Suhu (°C)",
        "Kelembapan": "Kelembapan (%)",
        "Status_Kategori": "Status",
    })
    st.dataframe(tabel, hide_index=True)
    st.download_button(
        "Unduh data terfilter (CSV)",
        data=dff.to_csv(index=False).encode("utf-8"),
        file_name="data_pemantauan_terfilter.csv",
        mime="text/csv",
    )

st.caption("Sumber: data dummy untuk demonstrasi. Ambang kategori disederhanakan.")
