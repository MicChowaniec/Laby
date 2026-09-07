# Lab 4 - testy statystyczne

Pytanie: czy rozkład jakości różni się między winem czerwonym i białym oraz czy alkohol wiąże się z jakością? Sprawdzana jest normalność i równość wariancji, stosowany jest test Manna-Whitneya oraz korelacja Spearmana. Poziom istotności wynosi `α = 0,05`.

## Hipotezy i reguła decyzji

- Mann-Whitney: H0 zakłada takie same rozkłady jakości w obu grupach; H1 zakłada różnicę rozkładów.
- Spearman: H0 zakłada `ρ = 0`; H1 zakłada `ρ ≠ 0`.
- H0 zostaje odrzucona wyłącznie wtedy, gdy `p-value < α`. W przeciwnym przypadku nie ma podstaw do odrzucenia H0.

## Wnioski

- Rozkłady jakości odbiegają od normalności, dlatego zastosowano test nieparametryczny.
- Dla porównania typów wina uzyskano `p = 3,63e-23`; H0 zostaje odrzucona. Efekt rank-biserial dla kolejności `red - white` wynosi około `-0,154`, co wskazuje na niższe rangi jakości wina czerwonego.
- Dla zależności alkoholu i jakości uzyskano `ρ = 0,447` oraz `p < 0,001`; H0 zostaje odrzucona. Zależność jest dodatnia i umiarkowana.

Wyniki są zapisywane w `wyniki/wyniki_testow.csv`, a sprawdzenie normalności i jednorodności wariancji w `wyniki/testy_zalozen.csv`.
