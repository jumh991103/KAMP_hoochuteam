# CN7 공식 산출물

`python run_cn7.py`로 모델 학습과 OOF 평가를 수행하고, `python run_cn7_temporal_ood.py`, `python run_cn7_test.py`를 순차 실행함.
내부 5-Seed Group-OOF PR-AUC 0.8164 ± 0.0181; Risk Only TP14 FP7 FN3(21건, 1.73%); Risk+Uncertainty TP15 FP10 FN2(25건, 2.06%).
E4/E5는 제품행과 Cycle 단위가 다르며 OOD 안전계층은 사후 추가 분석임.
`cn7_metrics.csv`, `cn7_oof_prediction.csv`, `cn7_threshold_result.csv`, `cn7_temporal_ood_*`, `cn7_test_*`를 각각의 근거로 사용함.
