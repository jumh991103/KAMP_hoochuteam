"""경진대회 제출 전 CSV-README 정합성 점검. 각 폴더에서 별도 모델 실행 후 사용."""
from pathlib import Path
import pandas as pd

ROOT=Path(__file__).resolve().parent
cn=ROOT/'CN7';rg=ROOT/'RG3'

# CN7: 5-seed OOF and policy confusion matrices
m=pd.read_csv(cn/'outputs/cn7_metrics.csv')
mean=m[m.Scope.eq('PerSeed_Mean')].iloc[0]
std=m[m.Scope.eq('PerSeed_Std')].iloc[0]
a=m[m.Policy.eq('Risk_Only')].iloc[-1]
b=m[m.Policy.eq('Risk_Plus_Uncertainty')].iloc[-1]
assert abs(mean.PR_AUC-0.8164355928)<1e-7
assert abs(std.PR_AUC-0.0180950846)<1e-7
assert (int(a.TP),int(a.FP),int(a.FN),int(a.Flag_Count))==(14,7,3,21)
assert (int(b.TP),int(b.FP),int(b.FN),int(b.Flag_Count))==(15,10,2,25)

# RG3: metrics derived from re-executed outputs, not hardcoded README claims
rm=pd.read_csv(rg/'outputs/rg3_metrics.csv')
rt=pd.read_csv(rg/'outputs/rg3_temporal_validation.csv')
cy=pd.read_csv(rg/'outputs/rg3_cycle_oot_metrics.csv').iloc[0]
oof=pd.read_csv(rg/'outputs/rg3_oof_prediction.csv')
hold=pd.read_csv(rg/'outputs/rg3_holdout_prediction.csv')
test=pd.read_csv(rg/'outputs/rg3_risk_prediction.csv',low_memory=False)
assert rm.shape[0]==5 and rt.shape[0]==3 and len(oof)==447 and len(hold)==250
for k in range(3):
 x=rm.iloc[k];y=rt.iloc[k]
 assert abs(x.PR_AUC-y.PR_AUC)<1e-12
assert abs(rm.iloc[3].PR_AUC-0.0414607261006366)<1e-9
assert abs(rm.iloc[4].PR_AUC-cy.PR_AUC)<1e-12
assert len(test)==35941 and test.Risk_Score.notna().sum()==17136
assert test.loc[test.RH_LH.eq('LH'),'Risk_Score'].isna().all()
assert len(pd.read_csv(rg/'outputs/rg3_inference_result.csv',low_memory=False))==len(test)
print('PASS: CN7 official metrics, RG3 rolling/holdout/cycle/OOF/inference aligned')
