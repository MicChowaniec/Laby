# Lab 5 - rozszerzona redukcja wymiarowości

PCA z wyborem liczby komponentów oraz ilościową oceną użyteczności reprezentacji przez porównanie regresji logistycznej dla klasy `quality >= 7` w pięciokrotnej walidacji krzyżowej.

## Zasady logiczne

- Liczba komponentów dla wariancji jest najmniejszym `k`, dla którego `cumulative_variance >= 0.90`.
- Najlepsza reprezentacja według modelu to wariant z największą średnią wartością ROC AUC.

## Wnioski

- Próg 90% wariancji zostaje osiągnięty przy 7 komponentach.
- Najwyższe średnie ROC AUC wynosi około `0,809` i zostało uzyskane dla 11 komponentów.
- Redukcja do 7 komponentów zapewnia kompresję, ale pełny zestaw komponentów daje nieco lepszy wynik predykcyjny.
- Dobór liczby komponentów powinien uwzględniać zarówno wariancję, jak i wynik walidacji.

Wyniki są zapisywane w `wyniki/ocena_reprezentacji.csv` i `podsumowanie.csv`.
