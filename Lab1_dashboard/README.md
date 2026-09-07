# Dashboard laboratoriów 1-6

Wielostronicowa aplikacja obejmuje wszystkie wykonane laboratoria:

- Lab 1 - dashboard decyzyjny,
- Lab 2 - eksploracyjna analiza danych,
- Lab 3 - PCA i t-SNE,
- Lab 4 - testy statystyczne,
- Lab 5 - ocena reprezentacji PCA,
- Lab 6 - analiza szeregu czasowego.

## Problem analityczny

Które właściwości fizykochemiczne odróżniają czerwone i białe wina oraz wiążą się z wysoką oceną jakości? Dashboard wspiera technologa jakości w wyborze zakresów parametrów do dalszej kontroli procesu.

## Źródła i łączenie

Wykorzystano dwa źródła UCI: `winequality-red.csv` i `winequality-white.csv`. Mają identyczny schemat; są łączone pionowo (union/concat), a kolumna `wine_type` zachowuje pochodzenie rekordu. Źródło: https://archive.ics.uci.edu/dataset/186/wine+quality

## KPI

- liczba próbek (wartość absolutna),
- średnia jakość,
- udział win wysokiej jakości (`quality >= 7`, wartość względna),
- zmiana średniej jakości względem całego, nieprzefiltrowanego zbioru.

## Uruchomienie

`.\run_dashboard.ps1`
