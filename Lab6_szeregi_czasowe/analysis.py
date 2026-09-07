from pathlib import Path
import sys
import warnings
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import pandas as pd, numpy as np, matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller,kpss
from statsmodels.tools.sm_exceptions import InterpolationWarning
from statsmodels.graphics.tsaplots import plot_acf,plot_pacf
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.metrics import mean_absolute_error
from common import DATA,outdir
out=outdir(__file__); df=pd.read_csv(DATA/"co2_mauna_loa.csv",parse_dates=["date"]); s=df.set_index("date").co2_ppm.asfreq("W-SAT"); missing=int(s.isna().sum()); s=s.interpolate().bfill().ffill()
dec=seasonal_decompose(s,model="additive",period=52,extrapolate_trend="period"); fig=dec.plot(); fig.set_size_inches(12,8); fig.tight_layout(); fig.savefig(out/"dekompozycja.png",dpi=160); plt.close(fig)
adf=adfuller(s,result_object=False)
with warnings.catch_warnings():
    warnings.simplefilter("ignore", InterpolationWarning)
    kp=kpss(s,regression="ct",nlags="auto",result_object=False)
d=s.diff().dropna(); adfd=adfuller(d,result_object=False)
fig,ax=plt.subplots(2,1,figsize=(10,7)); plot_acf(d,lags=60,ax=ax[0]); plot_pacf(d,lags=60,ax=ax[1],method="ywm"); plt.tight_layout(); plt.savefig(out/"acf_pacf.png",dpi=160); plt.close()
h=104; train,test=s.iloc[:-h],s.iloc[-h:]; model=ExponentialSmoothing(train,trend="add",seasonal="add",seasonal_periods=52,initialization_method="estimated").fit(); pred=model.forecast(h); seasonal_values=np.tile(train.iloc[-52:].to_numpy(),int(np.ceil(h/52)))[:h]; naive=pd.Series(seasonal_values,index=test.index); mae=mean_absolute_error(test,pred); mae0=mean_absolute_error(test,naive)
plt.figure(figsize=(12,5)); plt.plot(train.iloc[-260:],label="train"); plt.plot(test,label="test"); plt.plot(pred,label="Holt-Winters"); plt.legend(); plt.tight_layout(); plt.savefig(out/"prognoza.png",dpi=160); plt.close()
if mae < mae0:
    better_model = "Holt-Winters"
elif mae0 < mae:
    better_model = "seasonal-naive"
else:
    better_model = "remis"

pd.DataFrame([{
    "braki_przed_interpolacja": missing,
    "ADF_poziom_stat": adf[0], "ADF_poziom_p": adf[1],
    "KPSS_trend_stat": kp[0], "KPSS_trend_p_granica_gorna": kp[1],
    "ADF_roznica_stat": adfd[0], "ADF_roznica_p": adfd[1],
    "MAE_Holt_Winters": mae, "MAE_seasonal_naive": mae0,
    "lepszy_model_wg_MAE": better_model,
}]).to_csv(out/"podsumowanie.csv", index=False)
