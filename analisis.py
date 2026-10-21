"""Analisis detail dataset pengamatan cuaca."""
import pandas as pd, numpy as np
from scipy import stats

df = pd.read_csv("data_cuaca_sintesis.csv")
S, H = "Suhu (°C)", "Kelembaban (%)"
def judul(t): print("\n" + "="*70 + f"\n{t}\n" + "="*70)
def iqr_b(s):
    q1, q3 = s.quantile([.25, .75]); i = q3 - q1; return q1 - 1.5*i, q3 + 1.5*i

judul("1. KUALITAS DATA")
print(df.dtypes, "\nMissing:\n", df.isna().sum(), "\nDuplikat:", df.duplicated().sum())
print(f"Kelembaban di luar 0-100: {((df[H]<0)|(df[H]>100)).sum()} | Kelembaban tepat 100%: {(df[H]==100).sum()} (batas atas fisik)")

judul("2. NOMINAL: Kota & Kondisi")
for c in ["Kota", "Kondisi"]:
    f = df[c].value_counts(); print(pd.DataFrame({"n": f, "%": (f/len(df)*100).round(1)}), "\n")

judul("3. KOTA x KONDISI (% per kota) + uji Chi-Square")
ct = pd.crosstab(df.Kota, df.Kondisi); print((pd.crosstab(df.Kota, df.Kondisi, normalize="index")*100).round(1))
chi, p, dof, _ = stats.chi2_contingency(ct)
v = np.sqrt(chi / (ct.values.sum() * (min(ct.shape) - 1)))
print(f"\nChi-square={chi:.1f}, dof={dof}, p={p:.3g}, Cramer's V={v:.2f} ->", "kondisi cuaca berhubungan dengan kota" if p < .05 else "tidak ada hubungan signifikan")

judul("4. SUHU (Interval) & KELEMBABAN (Rasio): statistik deskriptif")
d = df[[S, H]].describe().T; d["skewness"] = df[[S, H]].skew(); d["kurtosis"] = df[[S, H]].kurt(); print(d.round(2))
for c in [S, H]:
    lo, hi = iqr_b(df[c]); o = df[(df[c] < lo) | (df[c] > hi)]
    print(f"\nOutlier {c}: batas [{lo:.1f}, {hi:.1f}] -> {len(o)} data ({len(o)/len(df)*100:.1f}%)")
    print(f"  Shapiro p={stats.shapiro(df[c].sample(500, random_state=1))[1]:.3g}")

judul("5. CATATAN SKALA: kenapa rasio suhu tidak berlaku?")
print("Suhu (interval): selisih bermakna, rasio tidak. 20 C bukan 2x lebih panas dari 10 C.")
print(f"Bukti: 20 C / 10 C = 2.00, tetapi dalam Kelvin 293.15 / 283.15 = {293.15/283.15:.3f}")
print("Kelembaban (rasio): 0% = tidak ada uap air, jadi 80% memang 2x lebih lembab dari 40%.")

judul("6. PER KOTA")
g = df.groupby("Kota").agg(n=(S, "size"), suhu_mean=(S, "mean"), suhu_sd=(S, "std"), hum_mean=(H, "mean"), hum_sd=(H, "std")).round(2)
print(g.sort_values("suhu_mean", ascending=False))
h1, p1 = stats.kruskal(*[x[S].values for _, x in df.groupby("Kota")])
h2, p2 = stats.kruskal(*[x[H].values for _, x in df.groupby("Kota")])
print(f"\nKruskal-Wallis Suhu ~ Kota: H={h1:.1f}, p={p1:.3g}\nKruskal-Wallis Kelembaban ~ Kota: H={h2:.1f}, p={p2:.3g}")

judul("7. PER KONDISI CUACA")
k = df.groupby("Kondisi").agg(n=(S, "size"), suhu_mean=(S, "mean"), hum_mean=(H, "mean"), hum_median=(H, "median")).round(2); print(k)
h1, p1 = stats.kruskal(*[x[S].values for _, x in df.groupby("Kondisi")])
h2, p2 = stats.kruskal(*[x[H].values for _, x in df.groupby("Kondisi")])
print(f"\nKruskal-Wallis Suhu ~ Kondisi: H={h1:.1f}, p={p1:.3g}\nKruskal-Wallis Kelembaban ~ Kondisi: H={h2:.1f}, p={p2:.3g}")

judul("8. KORELASI SUHU vs KELEMBABAN")
r, p = stats.spearmanr(df[S], df[H]); print(f"Gabungan: Spearman rho={r:+.2f}, p={p:.3g}")
print("Per kota:"); [print(f"  {kt:11s} rho={stats.spearmanr(x[S], x[H])[0]:+.2f}") for kt, x in df.groupby("Kota")]

judul("9. KATEGORI SUHU (turunan dari interval)")
kat = pd.cut(df[S], [0, 25, 30, 50], labels=["Sejuk (<=25)", "Hangat (25-30)", "Panas (>30)"]); print(kat.value_counts().sort_index())

judul("10. INSIGHT OTOMATIS")
print(f"- Kota terpanas (rata²): {g.suhu_mean.idxmax()} ({g.suhu_mean.max():.1f} C); terdingin: {g.suhu_mean.idxmin()} ({g.suhu_mean.min():.1f} C).")
print(f"- Kota paling lembab: {g.hum_mean.idxmax()} ({g.hum_mean.max():.1f}%).")
print(f"- Kondisi terbanyak: {df.Kondisi.value_counts().idxmax()} ({df.Kondisi.value_counts().max()/len(df)*100:.1f}%).")
print(f"- Saat Hujan kelembaban rata² {k.loc['Hujan','hum_mean']:.1f}% vs Cerah {k.loc['Cerah','hum_mean']:.1f}%.")
print(f"- Korelasi suhu-kelembaban {r:+.2f}: makin panas, cenderung makin kering.")
