# Lab 2 - eksploracyjna analiza danych

Analiza obejmuje strukturę i typy danych, braki, duplikaty, statystyki opisowe, rozkłady, IQR, korelacje, scatterplot, pairplot i heatmapę. Zbiór ma 6497 obserwacji i 11 bazowych zmiennych numerycznych.

## Wnioski

- Nie stwierdzono braków danych.
- Najsilniejsza korelacja liniowa z jakością dotyczy alkoholu (`r = 0,444`), a następna gęstości (`r = -0,306`).
- Metoda IQR wskazuje liczne wartości skrajne. Nie są one automatycznie usuwane, ponieważ mogą opisywać prawidłowe próbki.
- Typ wina stanowi ważny segment, gdyż rozkłady wielu parametrów różnią się między winem czerwonym i białym.
- Pojedyncza cecha nie wystarcza do jednoznacznego przewidywania jakości.

Wyniki liczbowe są zapisywane w `wyniki/podsumowanie.csv`, `statystyki_opisowe.csv` i `outliery_iqr.csv`.
