from pathlib import Path
import pandas as pd
from statsmodels.datasets import co2

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)
URLS = {
    "red": "https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv",
    "white": "https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-white.csv",
}
parts = []
for kind, url in URLS.items():
    df = pd.read_csv(url, sep=";")
    df["wine_type"] = kind
    df["source_url"] = url
    df.to_csv(DATA / f"winequality-{kind}.csv", index=False)
    parts.append(df)
pd.concat(parts, ignore_index=True).to_csv(DATA / "winequality-all.csv", index=False)

series = co2.load_pandas().data.reset_index()
series.columns = ["date", "co2_ppm"]
series.to_csv(DATA / "co2_mauna_loa.csv", index=False)
print(f"Zapisano {sum(map(len, parts))} rekordów wina i {len(series)} rekordów CO2.")
