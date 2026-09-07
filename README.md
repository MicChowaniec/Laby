# Pakiet laboratoriów 1-6

Wspólny temat: **czynniki fizykochemiczne wpływające na jakość czerwonego i białego wina**.

## Struktura

- `Lab1_dashboard/` - wielostronicowy dashboard Streamlit prezentujący Lab 1-6.
- `Lab2_EDA/` - pełna eksploracyjna analiza danych.
- `Lab3_redukcja_wymiarowosci/` - PCA i t-SNE.
- `Lab4_testy_statystyczne/` - hipotezy, sprawdzenie założeń, testy i interpretacja.
- `Lab5_redukcja_wymiarowosci/` - rozszerzona redukcja wymiarowości (PCA + analiza jakości reprezentacji).
- `Lab6_szeregi_czasowe/` - analiza szeregu CO2 (rozszerzenie opcjonalne z instrukcji).


## Uruchomienie:

```powershell
.\run_all.ps1
.\run_dashboard.ps1
```

Pierwsze polecenie tworzy lokalne środowisko `.venv`, instaluje w nim zależności,
przygotowuje dane i wykonuje Lab 2-6. Drugie uruchamia wspólny dashboard Lab 1-6.

Wymagany jest Python 3.10

## Źródła

- Cortez et al. (2009), UCI Machine Learning Repository, Wine Quality: https://archive.ics.uci.edu/dataset/186/wine+quality
- Mauna Loa CO2, pakiet `statsmodels` (oryginalnie NOAA): https://www.statsmodels.org/stable/datasets/generated/co2.html
