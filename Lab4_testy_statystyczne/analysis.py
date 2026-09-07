from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scipy import stats
import pandas as pd
from common import load_wine,outdir
df=load_wine(); out=outdir(__file__); a=df.loc[df.wine_type.eq("red"),"quality"]; b=df.loc[df.wine_type.eq("white"),"quality"]
sa=stats.shapiro(a.sample(min(2000,len(a)),random_state=42)); sb=stats.shapiro(b.sample(min(2000,len(b)),random_state=42)); lev=stats.levene(a,b)
mw=stats.mannwhitneyu(a,b,alternative="two-sided"); rbc=2*mw.statistic/(len(a)*len(b))-1; rho,p=stats.spearmanr(df.alcohol,df.quality)
alpha=.05

reject_mw = mw.pvalue < alpha
reject_spearman = p < alpha

assumptions = pd.DataFrame([
    {"test": "Shapiro-Wilk red", "statystyka": sa.statistic, "p_value": sa.pvalue},
    {"test": "Shapiro-Wilk white", "statystyka": sb.statistic, "p_value": sb.pvalue},
    {"test": "Levene red vs white", "statystyka": lev.statistic, "p_value": lev.pvalue},
])
assumptions.to_csv(out/"testy_zalozen.csv", index=False)

results = pd.DataFrame([
    {
        "test": "Mann-Whitney: quality red vs white",
        "statystyka": mw.statistic,
        "p_value": mw.pvalue,
        "alpha": alpha,
        "odrzucenie_H0": reject_mw,
        "wielkosc_efektu": rbc,
    },
    {
        "test": "Spearman: alcohol vs quality",
        "statystyka": rho,
        "p_value": p,
        "alpha": alpha,
        "odrzucenie_H0": reject_spearman,
        "wielkosc_efektu": rho,
    },
])
results.to_csv(out/"wyniki_testow.csv", index=False)
print(results.to_string(index=False))
