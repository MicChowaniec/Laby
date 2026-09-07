from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import numpy as np,pandas as pd,matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold,cross_val_score
from common import load_wine,outdir
df=load_wine(); out=outdir(__file__); X=df.select_dtypes("number").drop(columns="quality"); y=df.quality.ge(7).astype(int); Z=StandardScaler().fit_transform(X); p=PCA().fit(Z); cum=np.cumsum(p.explained_variance_ratio_); k90=int(np.searchsorted(cum,.9)+1)
cv=StratifiedKFold(5,shuffle=True,random_state=42); rows=[]
for k in range(2,X.shape[1]+1):
 model=make_pipeline(StandardScaler(),PCA(n_components=k),LogisticRegression(max_iter=2000,class_weight="balanced")); s=cross_val_score(model,X,y,cv=cv,scoring="roc_auc"); rows.append((k,s.mean(),s.std()))
res=pd.DataFrame(rows,columns=["komponenty","ROC_AUC_mean","ROC_AUC_std"]); res.to_csv(out/"ocena_reprezentacji.csv",index=False); best=res.loc[res.ROC_AUC_mean.idxmax()]
plt.errorbar(res.komponenty,res.ROC_AUC_mean,yerr=res.ROC_AUC_std,marker="o"); plt.axvline(k90,color="red",ls="--",label=f"90% wariancji: {k90}"); plt.xlabel("Liczba PC"); plt.ylabel("ROC AUC (5-fold CV)"); plt.legend(); plt.tight_layout(); plt.savefig(out/"jakosc_reprezentacji.png",dpi=160); plt.close()
pd.DataFrame([{
    "prog_wariancji": 0.90,
    "komponenty_dla_progu": k90,
    "najlepsza_liczba_komponentow": int(best.komponenty),
    "najlepsze_ROC_AUC": best.ROC_AUC_mean,
    "ROC_AUC_std": best.ROC_AUC_std,
}]).to_csv(out/"podsumowanie.csv", index=False)
