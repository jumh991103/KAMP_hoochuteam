# RG3 공식 산출물 (2026-10-08 검증 기준)

`python run_all.py`가 모든 아래 산출물을 현재 코드로 새로 생성함.

| 산출물 | 범위·생성 위치 |
|---|---|
| `rg3_temporal_validation.csv` | Rolling 3 Fold의 평가표 |
| `rg3_oof_prediction.csv` | Rolling Temporal Validation 예측 447건(전체 591건 OOF 아님) |
| `rg3_holdout_prediction.csv` | Session 4~5, 250건 |
| `rg3_metrics.csv` | Rolling·Final Holdout·Cycle post-hoc, 단위 구분 |
| `rg3_cycle_*` | 11/04 35 Cycle, 사후 구조진단 |
| `rg3_risk_prediction.csv` | 공식 unlabeled 35,941개 제품 행 Risk Ranking |
| `rg3_inference_result.csv` | 상기 공식 추론 결과의 동일 내용 호환 복사본 |

최종 결과(현재 검증 환경): Rolling PR-AUC 0.313587 / 0.046489 / 0.096094; Final Holdout 0.041461; Cycle 0.412428.
저장 산출물은 코드 실행 결과와 대조했고 `rg3_metrics.csv`에 예전 Posthoc 값은 남기지 않음.
`--skip-test`에서는 공식 unlabeled 추론을 생략하므로 해당 두 추론 CSV가 새로 갱신되지 않음.
