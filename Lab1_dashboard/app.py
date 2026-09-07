from pathlib import Path
import sys
import warnings

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from scipy import stats
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from statsmodels.tsa.stattools import adfuller, kpss
from statsmodels.tools.sm_exceptions import InterpolationWarning

from common import DATA, load_wine

st.set_page_config(page_title="Analiza danych - laboratoria 1-6", page_icon="📊", layout="wide")

st.markdown(
    """
    <style>
    .block-container {padding-top: 1.5rem; padding-bottom: 3rem; max-width: 1450px;}
    [data-testid="stMetric"] {background:#f7f9fc; border:1px solid #dbe3ef; padding:14px; border-radius:10px;}
    h1, h2, h3 {letter-spacing:-0.02em;}
    .note {padding:12px 14px; border-left:4px solid #3568d4; background:#f3f7ff; border-radius:4px;}
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def wine_data():
    return load_wine()


@st.cache_data
def pca_data():
    df = wine_data()
    features = df.select_dtypes("number").drop(columns="quality")
    scaled = StandardScaler().fit_transform(features)
    model = PCA().fit(scaled)
    scores = model.transform(scaled)
    explained = pd.DataFrame(
        {
            "komponent": np.arange(1, len(model.explained_variance_ratio_) + 1),
            "udział": model.explained_variance_ratio_,
            "skumulowana": np.cumsum(model.explained_variance_ratio_),
        }
    )
    points = pd.DataFrame(scores[:, :3], columns=["PC1", "PC2", "PC3"])
    points["quality"] = df["quality"].astype(str)
    points["wine_type"] = df["wine_type"]
    loadings = pd.DataFrame(
        model.components_.T,
        index=features.columns,
        columns=[f"PC{i + 1}" for i in range(features.shape[1])],
    )
    return explained, points, loadings


def header(title, description):
    st.title(title)
    st.markdown(f'<div class="note">{description}</div>', unsafe_allow_html=True)


def hypothesis_decision(p_value, alpha):
    if pd.isna(p_value):
        return "Nie można wyznaczyć"
    if p_value < alpha:
        return "H0 odrzucona"
    return "Brak podstaw do odrzucenia H0"


def wine_filters(df, key):
    with st.sidebar:
        st.markdown("### Filtry danych wina")
        kinds = st.multiselect(
            "Typ wina", sorted(df.wine_type.unique()), default=sorted(df.wine_type.unique()), key=f"{key}_type"
        )
        quality = st.slider(
            "Jakość", int(df.quality.min()), int(df.quality.max()),
            (int(df.quality.min()), int(df.quality.max())), key=f"{key}_quality"
        )
        alcohol = st.slider(
            "Alkohol [%]", float(df.alcohol.min()), float(df.alcohol.max()),
            (float(df.alcohol.min()), float(df.alcohol.max())), key=f"{key}_alcohol"
        )
    return df[df.wine_type.isin(kinds) & df.quality.between(*quality) & df.alcohol.between(*alcohol)]


def page_lab1():
    df = wine_filters(wine_data(), "l1")
    header("Lab 1 · Dashboard decyzyjny", "Ocena właściwości fizykochemicznych związanych z jakością czerwonego i białego wina.")
    if df.empty:
        st.warning("Brak obserwacji dla wybranych filtrów.")
        return
    baseline = wine_data().quality.mean()
    cols = st.columns(4)
    cols[0].metric("Liczba próbek", f"{len(df):,}")
    cols[1].metric("Średnia jakość", f"{df.quality.mean():.2f}")
    cols[2].metric("Udział jakości ≥ 7", f"{df.quality.ge(7).mean() * 100:.1f}%")
    cols[3].metric("Zmiana jakości vs całość", f"{(df.quality.mean() / baseline - 1) * 100:+.1f}%")
    a, b = st.columns(2)
    a.plotly_chart(px.histogram(df, x="quality", color="wine_type", barmode="group", title="Rozkład ocen jakości"), use_container_width=True)
    trend = df.groupby(["wine_type", "quality"], as_index=False).alcohol.mean()
    b.plotly_chart(px.line(trend, x="quality", y="alcohol", color="wine_type", markers=True, title="Średni alkohol według jakości"), use_container_width=True)
    st.plotly_chart(px.scatter(df, x="alcohol", y="volatile acidity", color="quality", symbol="wine_type", opacity=.45, title="Alkohol, kwasowość lotna i jakość"), use_container_width=True)
    st.download_button("Eksport przefiltrowanych danych", df.to_csv(index=False).encode("utf-8"), "wine_filtered.csv", "text/csv")
    with st.expander("Źródła i sposób połączenia"):
        st.write("Dwa zbiory UCI Wine Quality mają ten sam schemat i zostały połączone pionowo. Kolumna `wine_type` identyfikuje źródło rekordu.")
        st.link_button("UCI Wine Quality", "https://archive.ics.uci.edu/dataset/186/wine+quality")


def page_lab2():
    df = wine_filters(wine_data(), "l2")
    header("Lab 2 · Eksploracyjna analiza danych", "Struktura, kompletność, rozkłady, wartości odstające i zależności między zmiennymi.")
    if df.empty:
        st.warning("Brak obserwacji dla wybranych filtrów.")
        return
    num = df.select_dtypes("number")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Obserwacje", f"{len(df):,}")
    c2.metric("Zmienne numeryczne", num.shape[1])
    c3.metric("Braki danych", int(df.isna().sum().sum()))
    c4.metric("Duplikaty", int(df.duplicated().sum()))
    variable = st.selectbox("Analizowana zmienna", list(num.columns), index=list(num.columns).index("alcohol"))
    a, b = st.columns(2)
    a.plotly_chart(px.histogram(df, x=variable, color="wine_type", marginal="box", opacity=.7, title=f"Rozkład: {variable}"), use_container_width=True)
    b.plotly_chart(px.box(df, x="wine_type", y=variable, color="wine_type", points="outliers", title=f"Wartości odstające: {variable}"), use_container_width=True)
    corr = num.corr()
    st.plotly_chart(px.imshow(corr, text_auto=".2f", color_continuous_scale="RdBu_r", zmin=-1, zmax=1, title="Macierz korelacji"), use_container_width=True)
    q1, q3 = num.quantile(.25), num.quantile(.75)
    outliers = ((num.lt(q1 - 1.5 * (q3 - q1))) | num.gt(q3 + 1.5 * (q3 - q1))).sum().sort_values(ascending=False)
    with st.expander("Statystyki opisowe i liczba obserwacji odstających"):
        st.dataframe(num.describe().T, use_container_width=True)
        st.dataframe(outliers.rename("liczba outlierów IQR"), use_container_width=True)
    best = corr["quality"].drop("quality").sort_values(key=abs, ascending=False)
    st.info(f"Najsilniejsza korelacja liniowa z jakością: {best.index[0]} (r = {best.iloc[0]:.3f}). Wartości odstające nie są automatycznie usuwane, ponieważ mogą opisywać prawidłowe próbki.")


def page_lab3():
    header("Lab 3 · Redukcja wymiarowości", "Standaryzacja cech, PCA, wyjaśniona wariancja, dobór liczby komponentów i projekcja danych.")
    explained, points, loadings = pca_data()
    threshold = st.sidebar.slider("Próg wyjaśnionej wariancji", .70, .99, .90, .01, key="l3_threshold")
    k = int(np.searchsorted(explained["skumulowana"].to_numpy(), threshold) + 1)
    c1, c2, c3 = st.columns(3)
    c1.metric("Komponenty dla progu", k)
    c2.metric("Wariancja PC1", f"{explained.udział.iloc[0] * 100:.1f}%")
    c3.metric("Wariancja PC1+PC2", f"{explained.udział.iloc[:2].sum() * 100:.1f}%")
    fig = px.line(explained, x="komponent", y="skumulowana", markers=True, title="Skumulowana wyjaśniona wariancja")
    fig.add_hline(y=threshold, line_dash="dash", line_color="#c33")
    fig.add_vline(x=k, line_dash="dot")
    st.plotly_chart(fig, use_container_width=True)
    sample = points.sample(min(3000, len(points)), random_state=42)
    st.plotly_chart(px.scatter(sample, x="PC1", y="PC2", color="quality", symbol="wine_type", opacity=.55, title="Projekcja PCA 2D"), use_container_width=True)
    selected_pc = st.selectbox("Współczynniki komponentu", list(loadings.columns[:5]))
    loading_plot = loadings[selected_pc].sort_values().reset_index()
    loading_plot.columns = ["cecha", "wartość"]
    st.plotly_chart(px.bar(loading_plot, x="wartość", y="cecha", orientation="h", title=f"Loadings: {selected_pc}"), use_container_width=True)
    st.info(f"Dla progu {threshold:.0%} wymagane jest {k} komponentów. Projekcja 2D upraszcza strukturę, lecz nie daje pełnej separacji klas jakości.")


def page_lab4():
    df = wine_filters(wine_data(), "l4")
    header("Lab 4 · Testy statystyczne", "Weryfikacja różnic jakości między typami wina oraz zależności między alkoholem i jakością.")
    if not {"red", "white"}.issubset(set(df.wine_type.unique())):
        st.warning("Do porównania grup wymagane jest wybranie obu typów wina.")
        return
    alpha = st.sidebar.select_slider("Poziom istotności α", options=[.01, .05, .10], value=.05, key="l4_alpha")
    red = df.loc[df.wine_type.eq("red"), "quality"]
    white = df.loc[df.wine_type.eq("white"), "quality"]
    mw = stats.mannwhitneyu(red, white, alternative="two-sided")
    rbc = 2 * mw.statistic / (len(red) * len(white)) - 1
    rho, p_corr = stats.spearmanr(df.alcohol, df.quality)
    rows = pd.DataFrame([
        {"test": "Manna-Whitneya: jakość red vs white", "statystyka": mw.statistic, "p": mw.pvalue, "efekt": rbc, "decyzja": hypothesis_decision(mw.pvalue, alpha)},
        {"test": "Spearmana: alkohol vs jakość", "statystyka": rho, "p": p_corr, "efekt": rho, "decyzja": hypothesis_decision(p_corr, alpha)},
    ])
    st.dataframe(rows.style.format({"statystyka": "{:.4g}", "p": "{:.3g}", "efekt": "{:.3f}"}), use_container_width=True, hide_index=True)
    a, b = st.columns(2)
    a.plotly_chart(px.violin(df, x="wine_type", y="quality", color="wine_type", box=True, points=False, title="Jakość według typu wina"), use_container_width=True)
    b.plotly_chart(px.scatter(df.sample(min(2500, len(df)), random_state=42), x="alcohol", y="quality", color="wine_type", opacity=.35, trendline="ols", title="Alkohol a jakość"), use_container_width=True)
    with st.expander("Hipotezy i dobór testów"):
        st.markdown("**Test Manna-Whitneya** — H0: rozkłady jakości są takie same; H1: rozkłady różnią się. Test nieparametryczny zastosowano ze względu na porządkową skalę jakości i brak normalności.\n\n**Korelacja Spearmana** — H0: ρ = 0; H1: ρ ≠ 0. Zastosowano miarę monotonicznej zależności niewymagającą normalności.")


def page_lab5():
    header("Lab 5 · Ocena reprezentacji PCA", "Dobór liczby komponentów na podstawie wariancji oraz skuteczności klasyfikacji wysokiej jakości w walidacji krzyżowej.")
    path = ROOT / "Lab5_redukcja_wymiarowosci" / "wyniki" / "ocena_reprezentacji.csv"
    results = pd.read_csv(path)
    metric = st.sidebar.selectbox("Miara prezentowana na wykresie", ["ROC_AUC_mean", "ROC_AUC_std"], key="l5_metric")
    best = results.loc[results.ROC_AUC_mean.idxmax()]
    c1, c2, c3 = st.columns(3)
    c1.metric("Najlepsza liczba PC", int(best.komponenty))
    c2.metric("Najlepsze ROC AUC", f"{best.ROC_AUC_mean:.3f}")
    c3.metric("Odchylenie CV", f"{best.ROC_AUC_std:.3f}")
    st.plotly_chart(px.line(results, x="komponenty", y=metric, markers=True, title="Jakość reprezentacji w walidacji 5-fold"), use_container_width=True)
    explained, _, _ = pca_data()
    merged = results.merge(explained[["komponent", "skumulowana"]], left_on="komponenty", right_on="komponent")
    st.plotly_chart(px.scatter(merged, x="skumulowana", y="ROC_AUC_mean", text="komponenty", size="komponenty", title="Kompresja a skuteczność modelu"), use_container_width=True)
    st.dataframe(results.style.format({"ROC_AUC_mean": "{:.4f}", "ROC_AUC_std": "{:.4f}"}), use_container_width=True, hide_index=True)
    st.info("Liczba komponentów powinna być dobierana jednocześnie na podstawie wyjaśnionej wariancji i wyniku walidacji, a nie tylko wykresu scree.")


def page_lab6():
    header("Lab 6 · Analiza szeregu czasowego", "Trend, sezonowość, stacjonarność i prognozowanie stężenia CO₂ na Mauna Loa.")
    data = pd.read_csv(DATA / "co2_mauna_loa.csv", parse_dates=["date"]).set_index("date").co2_ppm.asfreq("W-SAT")
    missing = int(data.isna().sum())
    series = data.interpolate().bfill().ffill()
    start, end = st.sidebar.slider("Zakres lat", int(series.index.year.min()), int(series.index.year.max()), (int(series.index.year.min()), int(series.index.year.max())), key="l6_years")
    view = series[(series.index.year >= start) & (series.index.year <= end)]
    roll = st.sidebar.slider("Okno średniej ruchomej (tygodnie)", 4, 104, 52, 4, key="l6_roll")
    chart = pd.DataFrame({"CO2": view, f"średnia {roll} tyg.": view.rolling(roll, center=True).mean()}).reset_index()
    st.plotly_chart(px.line(chart, x="date", y=["CO2", f"średnia {roll} tyg."], title="Stężenie atmosferycznego CO₂"), use_container_width=True)
    adf = adfuller(series, result_object=False)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", InterpolationWarning)
        kp = kpss(series, regression="ct", nlags="auto", result_object=False)
    diff_adf = adfuller(series.diff().dropna(), result_object=False)
    c1, c2, c3 = st.columns(3)
    c1.metric("Braki przed interpolacją", missing)
    c2.metric("ADF poziomu · p", f"{adf[1]:.3g}")
    c3.metric("ADF pierwszej różnicy · p", f"{diff_adf[1]:.3g}")
    result = pd.DataFrame({"test": ["ADF poziomu", "KPSS z trendem", "ADF pierwszej różnicy"], "statystyka": [adf[0], kp[0], diff_adf[0]], "p": [f"{adf[1]:.3g}", f"< {kp[1]:.3g}", f"{diff_adf[1]:.3g}"]})
    st.dataframe(result.style.format({"statystyka": "{:.4f}"}), use_container_width=True, hide_index=True)
    a, b = st.columns(2)
    a.image(str(ROOT / "Lab6_szeregi_czasowe" / "wyniki" / "dekompozycja.png"), caption="Dekompozycja addytywna")
    b.image(str(ROOT / "Lab6_szeregi_czasowe" / "wyniki" / "prognoza.png"), caption="Prognoza Holt-Winters")
    st.info("Szereg zawiera rosnący trend i sezonowość roczną. Po pierwszym różnicowaniu uzyskiwany jest wynik ADF wskazujący na stacjonarność. Model Holt-Winters osiąga niższy MAE niż sezonowa prognoza naiwna.")
    st.link_button("Opis zbioru CO₂", "https://www.statsmodels.org/stable/datasets/generated/co2.html")


PAGES = {
    "Lab 1 · Dashboard": page_lab1,
    "Lab 2 · EDA": page_lab2,
    "Lab 3 · PCA i t-SNE": page_lab3,
    "Lab 4 · Testy statystyczne": page_lab4,
    "Lab 5 · Ocena PCA": page_lab5,
    "Lab 6 · Szeregi czasowe": page_lab6,
}

with st.sidebar:
    st.title("Laboratoria 1–6")
    selected = st.radio("Nawigacja", list(PAGES), label_visibility="collapsed")
    st.caption("Wstępne przetwarzanie i wizualizacja danych")

PAGES[selected]()
