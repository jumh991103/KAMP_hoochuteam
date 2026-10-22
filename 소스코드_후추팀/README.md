# CN7 및 RG3 사출성형 품질위험 예측과 검사 우선순위 지원

제6회 K-인공지능 제조데이터 분석 경진대회 · 후추 팀 제출 코드임.

## 단일 진입점 및 실행 순서

CN7 디렉터리에서 `python run_cn7.py` → `python run_cn7_temporal_ood.py` → `python run_cn7_test.py` 순으로 실행함.
RG3 디렉터리에서 `python run_all.py`를 실행하면 전처리 → Rolling/Final Holdout 평가 → 모델 학습 → unlabeled 추론 → Cycle-level 사후 분석까지 생성함.
`python run_all.py --skip-test`는 대형 unlabeled 추론을 생략하며 이 경우 추론 CSV는 갱신되지 않음.
각 폴더 `requirements.lock.txt`가 이번 Python 3.13.5 Linux 실행에서 사용한 버전을 기록함. Windows 및 다른 Python 환경에서 수치가 똑같다는 보장은 없음.

## 기준 성능

- CN7 Group-OOF PR-AUC **0.8164 ± 0.0181** (5 Seeds). Risk Only TP14/FP7/FN3, Recall **82.35%**, 검사21건(1.73%). Risk+Uncertainty TP15/FP10/FN2, Recall **88.24%**, 검사25건(2.06%). E4 PCA-OOD Cycle 기준 Recall80%는 사후 보완실험임.
- RG3 RH 591건, Absolute EWMA5 + XGBoost. Python3.13.5/XGBoost3.1.3 코드 재실행 기준 Rolling Fold PR-AUC **0.313587 / 0.046489 / 0.096094**, Final Holdout PR-AUC **0.041461**, ROC-AUC **0.425417**.
- RG3 11/04 **사후 Cycle-level** OOT PR-AUC **0.412428**, ROC-AUC **0.683673** (35 Cycle 중 불량7). 독립 최종 Holdout 대체 아님.
- RG3 Test 추론: 총35,941 제품 행 중 RH17,136행에만 위험점수를 부여하고 LH18,805행은 자동판정을 보류함. unlabeled 데이터에 정답이 없으므로 Test 성능 수치 없음.

## 검증·해석 유의사항

`python verify_submission.py`를 `final/` 디렉터리에서 실행해 출력 CSV와 성능 기준값을 확인함. 노트북은 탐색 기록으로 제공하며 오래된 저장 출력과 환경 절대경로를 제거함. **노트북 전체 재실행은 별도로 수행하지 않았고** 스크립트가 최종 재현 기준임. 모델 일반화 성능은 제한적이며 자동 합불 판정에 사용하지 않음.
RG3의 실시간 분포변화 감지기는 코드에 구현되어 있지 않으며, 이는 **향후 현장 운영 제안**으로 문서화함.
