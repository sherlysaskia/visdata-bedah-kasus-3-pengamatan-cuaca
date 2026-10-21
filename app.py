import pandas as pd, numpy as np, plotly.express as px, plotly.graph_objects as go
import streamlit as st
from scipy import stats

st.set_page_config(page_title="Dashboard Cuaca - Sherly Saskia Rani - 241051002", page_icon="🌦️", layout="wide")
S, H = "Suhu (°C)", "Kelembaban (%)"
TIPE = pd.DataFrame({"Kolom": ["Kota", "Suhu (°C)", "Kelembaban (%)", "Kondisi"],
                     "Skala": ["Nominal", "Numerik - Interval", "Numerik - Rasio", "Nominal"],
                     "Visualisasi yang tepat": ["Bar / Pie Chart", "Histogram, Box Plot, Line (bukan rasio!)", "Histogram / Box Plot", "Bar / Pie Chart"]})
WARNA = {"Cerah": "#f1c40f", "Berawan": "#95a5a6", "Hujan": "#3498db", "Kabut": "#8e9aaf"}

@st.cache_data
def load():
    d = pd.read_csv("data_cuaca_sintesis.csv")
    d["Kategori Suhu"] = pd.cut(d[S], [0, 25, 30, 50], labels=["Sejuk (≤25)", "Hangat (25-30)", "Panas (>30)"])
    return d
df = load()

st.sidebar.header("🔎 Filter")
st.sidebar.markdown("**Sherly Saskia Rani**  \nNIM 241051002")
kota = st.sidebar.multiselect("Kota", sorted(df.Kota.unique()), default=sorted(df.Kota.unique()))
kond = st.sidebar.multiselect("Kondisi", sorted(df.Kondisi.unique()), default=sorted(df.Kondisi.unique()))
rs = st.sidebar.slider("Rentang suhu (°C)", float(df[S].min()), float(df[S].max()), (float(df[S].min()), float(df[S].max())), step=0.5)
rh = st.sidebar.slider("Rentang kelembaban (%)", int(df[H].min()), 100, (int(df[H].min()), 100))
f = df[df.Kota.isin(kota) & df.Kondisi.isin(kond) & df[S].between(*rs) & df[H].between(*rh)]
if f.empty:
    st.warning("Tidak ada data untuk filter ini."); st.stop()

st.title("🌦️ Dashboard Pengamatan Cuaca-Sherly Saskia Rani · NIM 241051002 ")
st.caption("Bedah Kasus 3· Data sintesis 1.000 pengamatan (dikembangkan dari 2 baris seed: Jakarta & Bandung)")

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Pengamatan", f"{len(f):,}".replace(",", "."))
c2.metric("Rata² Suhu", f"{f[S].mean():.1f} °C")
c3.metric("Rata² Kelembaban", f"{f[H].mean():.1f} %")
c4.metric("Kondisi Terbanyak", f.Kondisi.value_counts().idxmax())
c5.metric("Persentase Hujan", f"{(f.Kondisi == 'Hujan').mean()*100:.1f}%")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏷️ Nominal (Kota & Kondisi)", "🌡️ Interval (Suhu)", "💧 Rasio (Kelembaban)", "🔗 Korelasi & Uji", "🗂️ Data"])

with tab1:
    a, b = st.columns(2)
    kc = f.Kota.value_counts().reset_index(); kc.columns = ["Kota", "Jumlah"]
    a.plotly_chart(px.bar(kc.sort_values("Jumlah"), x="Jumlah", y="Kota", orientation="h", color="Jumlah", color_continuous_scale="Blues",
                          title="Jumlah Pengamatan per Kota"), width="stretch")
    kd = f.Kondisi.value_counts().reset_index(); kd.columns = ["Kondisi", "Jumlah"]
    b.plotly_chart(px.pie(kd, names="Kondisi", values="Jumlah", hole=.45, color="Kondisi", color_discrete_map=WARNA,
                          title="Proporsi Kondisi Cuaca"), width="stretch")
    ck = f.groupby(["Kota", "Kondisi"]).size().reset_index(name="Jumlah")
    st.plotly_chart(px.bar(ck, x="Kota", y="Jumlah", color="Kondisi", barmode="stack", color_discrete_map=WARNA,
                           title="Kondisi Cuaca per Kota"), width="stretch")
    pr = pd.crosstab(f.Kota, f.Kondisi, normalize="index").mul(100).round(1)
    st.plotly_chart(px.imshow(pr, text_auto=True, aspect="auto", color_continuous_scale="Blues",
                              title="Peluang kondisi cuaca per kota (%)"), width="stretch")

with tab2:
    st.info("**Suhu = skala interval.** Selisih bermakna (32,5 − 24,0 = 8,5 °C), tetapi **rasio tidak berlaku**: 20 °C bukan 2× lebih panas dari 10 °C, "
            "karena 0 °C bukan 'tidak ada suhu'. Dalam Kelvin, 293,15 / 283,15 hanya ≈ 1,035. Rata-rata dan selisih boleh dipakai, rasio tidak.")
    a, b = st.columns(2)
    nb = a.slider("Jumlah bin", 10, 50, 25, key="nb1")
    a.plotly_chart(px.histogram(f, x=S, nbins=nb, marginal="box", color_discrete_sequence=["#e67e22"], title="Distribusi Suhu"), width="stretch")
    b.plotly_chart(px.box(f, x="Kota", y=S, color="Kota", points="outliers", title="Sebaran & Outlier Suhu per Kota")
                   .update_layout(showlegend=False), width="stretch")
    c, d = st.columns(2)
    c.plotly_chart(px.box(f, x="Kondisi", y=S, color="Kondisi", color_discrete_map=WARNA, title="Suhu menurut Kondisi Cuaca")
                   .update_layout(showlegend=False), width="stretch")
    ks = f.groupby(["Kota", "Kategori Suhu"], observed=True).size().reset_index(name="Jumlah")
    d.plotly_chart(px.bar(ks, x="Kota", y="Jumlah", color="Kategori Suhu", title="Kategori Suhu per Kota",
                          color_discrete_sequence=["#3498db", "#f1c40f", "#e74c3c"]), width="stretch")
    m = f.groupby("Kota")[S].mean().sort_values().reset_index()
    st.plotly_chart(px.bar(m, x=S, y="Kota", orientation="h", text=m[S].round(1), title="Rata² Suhu per Kota (°C)"), width="stretch")

with tab3:
    st.info("**Kelembaban = skala rasio.** Nol absolut = benar-benar tidak ada uap air, sehingga 80% memang 2× lebih lembab dari 40%. Batas atas fisiknya 100%.")
    a, b = st.columns(2)
    nb2 = a.slider("Jumlah bin", 10, 50, 25, key="nb2")
    a.plotly_chart(px.histogram(f, x=H, nbins=nb2, marginal="box", color_discrete_sequence=["#3498db"], title="Distribusi Kelembaban"), width="stretch")
    b.plotly_chart(px.box(f, x="Kota", y=H, color="Kota", points="outliers", title="Sebaran & Outlier Kelembaban per Kota")
                   .update_layout(showlegend=False), width="stretch")
    st.plotly_chart(px.violin(f, x="Kondisi", y=H, color="Kondisi", box=True, color_discrete_map=WARNA,
                              title="Kelembaban menurut Kondisi Cuaca").update_layout(showlegend=False), width="stretch")
    dd = f[[S, H]].describe().T; dd["skewness"] = f[[S, H]].skew()
    st.dataframe(dd.round(2), width="stretch")

with tab4:
    a, b = st.columns(2)
    a.plotly_chart(px.scatter(f, x=S, y=H, color="Kondisi", color_discrete_map=WARNA, opacity=.65, title="Suhu vs Kelembaban"), width="stretch")
    cm = f[[S, H]].corr(method="spearman")
    b.plotly_chart(px.imshow(cm.round(2), text_auto=True, zmin=-1, zmax=1, color_continuous_scale="RdBu_r", title="Korelasi Spearman"), width="stretch")
    r, p = stats.spearmanr(f[S], f[H])
    st.info(f"**Spearman Suhu vs Kelembaban:** ρ = {r:.2f} (p = {p:.3g}). Cenderung negatif: makin panas, makin kering.")
    if f.Kota.nunique() > 1 and f.Kondisi.nunique() > 1:
        ct = pd.crosstab(f.Kota, f.Kondisi); chi, p2, dof, _ = stats.chi2_contingency(ct)
        v = np.sqrt(chi / (ct.values.sum() * (min(ct.shape) - 1)))
        st.info(f"**Chi-square Kota × Kondisi:** χ² = {chi:.1f}, p = {p2:.3g}, Cramér's V = {v:.2f} → "
                f"{'kondisi cuaca berhubungan dengan kota' if p2 < .05 else 'tidak ada hubungan signifikan'} (α = 0,05).")
    if f.Kondisi.nunique() > 1:
        hh, p3 = stats.kruskal(*[g[H].values for _, g in f.groupby("Kondisi")])
        st.info(f"**Kruskal-Wallis Kelembaban antar kondisi:** H = {hh:.1f}, p = {p3:.3g}.")
    per = pd.DataFrame({"Kota": k, "ρ": stats.spearmanr(x[S], x[H])[0]} for k, x in f.groupby("Kota") if len(x) > 3)
    if not per.empty:
        st.plotly_chart(px.bar(per.sort_values("ρ"), x="ρ", y="Kota", orientation="h", title="Spearman Suhu vs Kelembaban per Kota"), width="stretch")

with tab5:
    st.markdown("**Tipe data tiap kolom**")
    st.table(TIPE)
    st.dataframe(f.drop(columns="Kategori Suhu"), width="stretch", height=350)
    st.download_button("⬇️ Unduh CSV (terfilter)", f.to_csv(index=False).encode(), "cuaca_filtered.csv", "text/csv")
