# Lab 6 - analiza szeregu czasowego

Ponieważ wspólny zbiór win nie ma komponentu czasowego, użyto szeregu atmosferycznego CO₂ z Mauna Loa (statsmodels/NOAA). Analiza obejmuje braki, interpolację, trend i sezonowość, ADF, KPSS, ACF/PACF oraz prognozę Holt-Winters porównaną z naiwną metodą sezonową.

## Zasady logiczne

- Dla ADF H0 oznacza obecność pierwiastka jednostkowego. H0 zostaje odrzucona, gdy `p-value < 0,05`.
- Dla KPSS H0 oznacza stacjonarność względem trendu. H0 zostaje odrzucona, gdy `p-value < 0,05`.
- Lepszym modelem prognostycznym jest model z niższym MAE. W kodzie zastosowano jawne warunki `mae < mae0`, `mae0 < mae` oraz przypadek remisu.

## Wnioski

- Przed interpolacją występuje 59 brakujących wartości.
- Poziom szeregu jest niestacjonarny: ADF daje `p = 0,961`, a dla KPSS z trendem `p < 0,01`. Wartość `0,01` zwracana przez bibliotekę jest górną granicą tabeli, a nie dokładnym p-value.
- Pierwsza różnica jest stacjonarna według ADF (`p ≈ 1,3e-28`).
- Szereg wykazuje rosnący trend i sezonowość roczną.
- Holt-Winters osiąga `MAE = 0,475`, a seasonal-naive `MAE = 1,875`; według jawnego kryterium niższego MAE lepszy jest Holt-Winters.

Wyniki liczbowe są zapisywane w `wyniki/podsumowanie.csv`.
