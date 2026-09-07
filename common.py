from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"

def load_wine():
    path = DATA / "winequality-all.csv"
    if not path.exists():
        raise FileNotFoundError("Uruchom najpierw: python prepare_data.py")
    return pd.read_csv(path)

def outdir(script_file):
    p = Path(script_file).resolve().parent / "wyniki"
    p.mkdir(exist_ok=True)
    return p
