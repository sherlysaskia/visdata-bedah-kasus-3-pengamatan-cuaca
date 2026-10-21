# 🌦️ Dashboard Pengamatan Cuaca
🔗 **Demo:** https://dashboard-cuaca-sherly.streamlit.app

**Bedah Kasus 3 · Visualisasi Data**
Sherly Saskia Rani · NIM 241051002

Dashboard interaktif berbasis Streamlit untuk menganalisis data pengamatan cuaca. Dataset berisi **1.000 data sintesis** yang dikembangkan dari 2 baris seed pada materi kuliah (Jakarta dan Bandung).

## Data seed

| Kota | Suhu (°C) | Kelembaban (%) | Kondisi |
|---|---|---|---|
| Jakarta | 32,5 | 75 | Cerah |
| Bandung | 24,0 | 85 | Hujan |

Data sintesis dibangkitkan dengan asumsi: 8 kota, 4 kondisi cuaca (Cerah, Berawan, Hujan, Kabut), suhu lebih rendah dan kelembaban lebih tinggi saat hujan, serta sedikit kejadian suhu ekstrem sebagai outlier. Data ini hanya untuk latihan, bukan data pengamatan sebenarnya.

## Skala pengukuran data

| Kolom | Skala | Visualisasi |
|---|---|---|
| Kota, Kondisi | Nominal | Bar chart, pie chart |
| Suhu (°C) | Interval | Histogram, box plot |
| Kelembaban (%) | Rasio | Histogram, box plot, violin |

**Catatan:** suhu dalam °C adalah skala interval, jadi selisihnya bermakna tetapi rasionya tidak. 20 °C bukan 2× lebih panas dari 10 °C. Kelembaban punya nol absolut, sehingga 80% memang 2× lebih lembab dari 40%.

## Fitur dashboard

- 5 kartu KPI: jumlah pengamatan, rata-rata suhu, rata-rata kelembaban, kondisi terbanyak, persentase hujan
- Filter sidebar: kota, kondisi, rentang suhu, rentang kelembaban
- 5 tab: Nominal, Interval (Suhu), Rasio (Kelembaban), Korelasi & Uji, Data
- Uji statistik: Spearman, Chi-square (dengan Cramér's V), Kruskal-Wallis
- Deteksi outlier dengan metode IQR
- Unduh data hasil filter dalam format CSV

## Temuan utama

- Kota terpanas: Surabaya (rata-rata 32,0 °C). Kota terdingin dan paling lembab: Bandung (24,0 °C, kelembaban 83%).
- Kondisi terbanyak: Cerah (38,7%).
- Kelembaban rata-rata saat hujan 86,1%, sedangkan saat cerah 65,4%.
- Korelasi suhu dan kelembaban negatif kuat (Spearman ρ = −0,72): makin panas, makin kering.
- Hubungan kota dan kondisi cuaca signifikan (p < 0,001) tetapi lemah (Cramér's V = 0,14).

## Struktur file

| File | Fungsi |
|---|---|
| `generate_data.py` | Membangkitkan 1.000 data sintesis |
| `analisis.py` | Analisis statistik detail di terminal |
| `app.py` | Dashboard Streamlit |
| `data_cuaca_sintesis.csv` | Dataset hasil sintesis |
| `hasil_analisis.txt` | Keluaran `analisis.py` |
| `requirements.txt` | Daftar library |

## Cara menjalankan

```bash
pip install -r requirements.txt
python generate_data.py      # opsional, untuk membuat ulang data
python analisis.py           # opsional, analisis di terminal
streamlit run app.py
```

Dashboard terbuka di `http://localhost:8501`.

## Teknologi

Python · Pandas · NumPy · SciPy · Plotly · Streamlit
