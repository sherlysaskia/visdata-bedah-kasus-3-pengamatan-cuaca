"""Membangkitkan 1000 data sintesis pengamatan cuaca dari 2 baris seed Bedah Kasus 3."""
import numpy as np, pandas as pd
rng = np.random.default_rng(11)

# kota: (suhu dasar C, kelembaban dasar %, peluang [Cerah, Berawan, Hujan, Kabut])
KOTA = {
    "Jakarta":    (31.0, 72, [.40, .30, .27, .03]),   # seed
    "Bandung":    (25.0, 80, [.22, .30, .43, .05]),   # seed
    "Surabaya":   (32.0, 70, [.48, .27, .22, .03]),
    "Medan":      (30.5, 78, [.32, .30, .35, .03]),
    "Semarang":   (31.0, 74, [.42, .28, .27, .03]),
    "Yogyakarta": (29.5, 76, [.38, .30, .29, .03]),
    "Makassar":   (31.5, 73, [.46, .27, .24, .03]),
    "Denpasar":   (30.5, 75, [.44, .28, .25, .03]),
}
KOND = ["Cerah", "Berawan", "Hujan", "Kabut"]
# efek kondisi: (selisih suhu, selisih kelembaban)
EFEK = {"Cerah": (+2.0, -9), "Berawan": (0.0, 0), "Hujan": (-3.0, +10), "Kabut": (-2.5, +12)}
w = np.array([.17, .17, .13, .11, .13, .11, .10, .08]); w /= w.sum()

names = list(KOTA)
rows = []
for _ in range(1000):
    k = names[rng.choice(len(names), p=w)]
    ts, hs, pk = KOTA[k]
    c = KOND[rng.choice(4, p=pk)]
    dt, dh = EFEK[c]
    suhu = ts + dt + rng.normal(0, 1.4)
    hum = hs + dh + rng.normal(0, 6) - 0.9 * (suhu - ts - dt)   # makin panas -> sedikit lebih kering
    if rng.random() < 0.02: suhu += rng.choice([-1, 1]) * rng.uniform(4, 7)   # kejadian ekstrem (outlier)
    suhu = np.round(np.clip(suhu, 14, 40) * 2) / 2                              # presisi 0.5 C
    hum = int(np.clip(round(hum), 25, 100))                                     # batas atas fisik 100%
    rows.append((k, suhu, hum, c))

df = pd.DataFrame(rows, columns=["Kota", "Suhu (°C)", "Kelembaban (%)", "Kondisi"])
df.loc[0] = ["Jakarta", 32.5, 75, "Cerah"]      # seed 1 (asli)
df.loc[1] = ["Bandung", 24.0, 85, "Hujan"]      # seed 2 (asli)
df.to_csv("data_cuaca_sintesis.csv", index=False)
print(df.head(), "\nBaris:", len(df))
