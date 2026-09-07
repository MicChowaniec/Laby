# Lab 3 - redukcja wymiarowości

Standaryzacja 11 cech, PCA, wybór najmniejszej liczby komponentów wyjaśniających co najmniej 90% wariancji, wykres scree, projekcja 2D, loadings oraz t-SNE na reprezentatywnej próbce.

## Zasada doboru komponentów

Wybierana jest najmniejsza liczba `k`, dla której skumulowany udział wyjaśnionej wariancji jest większy lub równy `0,90`. Warunek jest realizowany bezpośrednio w kodzie przez `cum >= 0.90`.

## Wnioski

- Próg 90% wariancji zostaje osiągnięty przy 7 komponentach.
- Największe bezwzględne udziały w PC1 mają: całkowity SO₂, wolny SO₂ i kwasowość lotna.
- Projekcja PCA 2D nie rozdziela jednoznacznie ocen jakości.
- t-SNE lepiej uwidacznia lokalne sąsiedztwa, ale nie zachowuje globalnych odległości.

Wyniki liczbowe są zapisywane w `wyniki/podsumowanie.csv`, `wyjasniona_wariancja.csv` i `loadings.csv`.
