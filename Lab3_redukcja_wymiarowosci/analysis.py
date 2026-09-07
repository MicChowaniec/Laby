from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import numpy as np, pandas as pd, matplotlib.pyplot as plt, seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from common import load_wine,outdir
df=load_wine(); out=outdir(__file__); X=df.select_dtypes("number").drop(columns="quality"); Z=StandardScaler().fit_transform(X)
pca=PCA().fit(Z); cum=np.cumsum(pca.explained_variance_ratio_); k=int(np.searchsorted(cum,.90)+1); scores=pca.transform(Z)
pd.DataFrame({"PC":range(1,len(cum)+1),"udział":pca.explained_variance_ratio_,"skumulowana":cum}).to_csv(out/"wyjasniona_wariancja.csv",index=False)
plt.plot(range(1,len(cum)+1),cum,marker="o"); plt.axhline(.9,color="red",ls="--"); plt.axvline(k,color="gray",ls=":"); plt.xlabel("Liczba komponentów"); plt.ylabel("Skumulowana wariancja"); plt.tight_layout(); plt.savefig(out/"scree.png",dpi=160); plt.close()
plot=pd.DataFrame(scores[:,:2],columns=["PC1","PC2"]); plot["quality"]=df.quality.astype(str); plot["wine_type"]=df.wine_type
sns.scatterplot(data=plot.sample(min(2500,len(plot)),random_state=42),x="PC1",y="PC2",hue="quality",style="wine_type",alpha=.55,palette="viridis"); plt.tight_layout(); plt.savefig(out/"pca_2d.png",dpi=160); plt.close()
load=pd.DataFrame(pca.components_.T,index=X.columns,columns=[f"PC{i+1}" for i in range(X.shape[1])]); load.to_csv(out/"loadings.csv")
plt.figure(figsize=(8,6)); sns.heatmap(load.iloc[:,:5],annot=True,cmap="coolwarm",center=0); plt.tight_layout(); plt.savefig(out/"loadings.png",dpi=160); plt.close()
ix=df.sample(min(1500,len(df)),random_state=42).index; ts=TSNE(n_components=2,random_state=42,init="pca",learning_rate="auto",perplexity=35).fit_transform(Z[ix]);
plt.scatter(ts[:,0],ts[:,1],c=df.loc[ix,"quality"],cmap="viridis",s=10,alpha=.65); plt.colorbar(label="quality"); plt.tight_layout(); plt.savefig(out/"tsne_2d.png",dpi=160); plt.close()
top=load.PC1.abs().sort_values(ascending=False).head(3)
pd.DataFrame({
    "metryka": ["prog_wariancji", "liczba_komponentow", *[f"PC1_cecha_{i}" for i in range(1, 4)]],
    "wartosc": [0.90, k, *top.index],
}).to_csv(out/"podsumowanie.csv", index=False)
