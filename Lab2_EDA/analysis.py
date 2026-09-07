from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from common import load_wine,outdir

df=load_wine(); out=outdir(__file__); num=df.select_dtypes("number")
with open(out/"struktura.txt","w",encoding="utf-8") as f:
    f.write(f"Wymiary: {df.shape}\n\nTypy:\n{df.dtypes}\n\nBraki:\n{df.isna().sum()}\n\nDuplikaty: {df.duplicated().sum()}\n")
num.describe().T.to_csv(out/"statystyki_opisowe.csv")
q1=num.quantile(.25); q3=num.quantile(.75); iqr=q3-q1
((num.lt(q1-1.5*iqr))|num.gt(q3+1.5*iqr)).sum().sort_values(ascending=False).rename("liczba_outlierow_IQR").to_csv(out/"outliery_iqr.csv")
plt.figure(figsize=(14,9)); sns.heatmap(num.corr(),cmap="coolwarm",center=0); plt.tight_layout(); plt.savefig(out/"korelacje.png",dpi=160); plt.close()
fig,axs=plt.subplots(2,3,figsize=(14,8));
for ax,c in zip(axs.flat,["alcohol","volatile acidity","density","sulphates","residual sugar","quality"]): sns.histplot(data=df,x=c,hue="wine_type",kde=True,ax=ax,element="step")
plt.tight_layout(); plt.savefig(out/"rozkłady.png",dpi=160); plt.close()
s=df.sample(min(1200,len(df)),random_state=42)
sns.pairplot(s,vars=["alcohol","volatile acidity","density","sulphates","quality"],hue="wine_type",corner=True,plot_kws={"alpha":.35,"s":12}); plt.savefig(out/"pairplot.png",dpi=140); plt.close()
plt.figure(figsize=(10,5)); sns.boxplot(data=df,x="wine_type",y="alcohol",hue="wine_type"); plt.tight_layout(); plt.savefig(out/"boxplot_alkohol.png",dpi=160); plt.close()
corr=num.corr()["quality"].drop("quality").sort_values(key=abs,ascending=False)
summary = pd.DataFrame({
    "metryka": ["obserwacje", "zmienne_numeryczne", "braki", "najsilniejsza_korelacja", "r"],
    "wartosc": [len(df), num.shape[1], int(df.isna().sum().sum()), corr.index[0], corr.iloc[0]],
})
summary.to_csv(out/"podsumowanie.csv", index=False)
print(summary.to_string(index=False))
