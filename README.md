# Pakiet laboratoriów 1-6

Wspólny temat: **czynniki fizykochemiczne wpływające na jakość czerwonego i białego wina**.

## Struktura

- `Lab1_dashboard/` - wielostronicowy dashboard Streamlit prezentujący Lab 1-6.
- `Lab2_EDA/` - pełna eksploracyjna analiza danych.
- `Lab3_redukcja_wymiarowosci/` - PCA i t-SNE.
- `Lab4_testy_statystyczne/` - hipotezy, sprawdzenie założeń, testy i interpretacja.
- `Lab5_redukcja_wymiarowosci/` - rozszerzona redukcja wymiarowości (PCA + analiza jakości reprezentacji).
- `Lab6_szeregi_czasowe/` - analiza szeregu CO2 (rozszerzenie opcjonalne z instrukcji).

## Uruchomienie na Windows (najprościej)

W PowerShell, będąc w katalogu projektu:

```powershell
.\run_all.ps1
.\run_dashboard.ps1
```

Pierwsze polecenie tworzy lokalne środowisko `.venv`, instaluje w nim zależności,
przygotowuje dane i wykonuje Lab 2-6. Drugie uruchamia wspólny dashboard Lab 1-6.

Wymagany jest Python 3.10 lub nowszy dostępny jako `py` albo `python`. Można go pobrać z
https://www.python.org/downloads/ (podczas instalacji należy zaznaczyć `Add Python to PATH`).

Alternatywnie Python 3.12 można zainstalować w PowerShell przez Menedżera pakietów Windows:

```powershell
winget install -e --id Python.Python.3.12
```

Po instalacji należy zamknąć i ponownie otworzyć PowerShell, przejść do katalogu projektu
i uruchomić `./run_all.ps1`. Skrypt sprawdza kompletność `.venv`; brakujący `pyvenv.cfg`
powoduje automatyczne odtworzenie środowiska przez `python -m venv --clear`.

Jeżeli PowerShell blokuje lokalne skrypty, użyj:

```powershell
powershell -ExecutionPolicy Bypass -File .\run_all.ps1
powershell -ExecutionPolicy Bypass -File .\run_dashboard.ps1
```

## Uruchomienie ręczne (gdy Python jest w PATH)

```powershell
python -m pip install -r requirements.txt
python prepare_data.py
python Lab2_EDA/analysis.py
python Lab3_redukcja_wymiarowosci/analysis.py
python Lab4_testy_statystyczne/analysis.py
python Lab5_redukcja_wymiarowosci/analysis.py
python Lab6_szeregi_czasowe/analysis.py
streamlit run Lab1_dashboard/app.py
```

Wyniki skryptów trafiają do podfolderów `wyniki/`. Każdy lab ma własny README z opisem zadania, metod i interpretacji.

## Źródła

- Cortez et al. (2009), UCI Machine Learning Repository, Wine Quality: https://archive.ics.uci.edu/dataset/186/wine+quality
- Mauna Loa CO2, pakiet `statsmodels` (oryginalnie NOAA): https://www.statsmodels.org/stable/datasets/generated/co2.html
- Treść i kryteria wykonania: przekazane materiały Lab 1-6.
