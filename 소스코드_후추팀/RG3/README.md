## 보고서 제6장 기준 제출 구조

```text
RG3/
├─ data/
│  ├─ raw/
│  │  ├─ moldset_labeled_rg3.csv
│  │  ├─ labeled_data.csv
│  │  ├─ moldset_unlabeled_rg3.csv
│  │  └─ unlabeled_data.csv
│  └─ processed/
│     ├─ train_rg3_preprocessed.csv
│     └─ rg3_model_input.csv
├─ src/
│  ├─ __init__.py
│  ├─ config_rg3.py
│  ├─ preprocess_rg3.py
│  ├─ feature_engineering_rg3.py
│  ├─ train_rg3.py
│  ├─ evaluate_rg3.py
│  ├─ inference_rg3.py
│  └─ cycle_analysis_rg3.py
├─ models/
│  └─ rg3_xgb_final.pkl
├─ outputs/
│  ├─ rg3_metrics.csv
│  ├─ rg3_oof_prediction.csv
│  ├─ rg3_temporal_validation.csv
│  ├─ rg3_holdout_prediction.csv
│  ├─ rg3_inference_result.csv
│  ├─ rg3_risk_prediction.csv
│  ├─ rg3_cycle_side_summary.csv
│  ├─ rg3_cycle_session_summary.csv
│  ├─ rg3_cycle_oot_metrics.csv
│  ├─ rg3_cycle_oot_predictions.csv
│  └─ rg3_cycle_inspection_tradeoff.csv
├─ notebooks/
│  ├─ rg3_analysis.ipynb
│  └─ rg3_cycle_analysis.ipynb
├─ run_rg3.py
├─ run_rg3_cycle_analysis.py
├─ requirements.txt
└─ README.md
```

> 보고서 본문의 디렉터리 표에는 `rg3_inference_result.csv`가, 파일 역할 설명에는
> `rg3_risk_prediction.csv`가 기재되어 있어 두 이름을 모두 포함함.
> 두 파일은 동일한 신규 데이터 Risk Ranking 결과를 가리킴.


# RG3 제조 불량 Risk Ranking 모델

KAMP 사출성형 제조데이터 중 **RG3 생산데이터의 불량 위험도를 분석하고 검사 우선순위를 지원하기 위한 머신러닝 모델**입니다.

RG3에서는 전체 불량이 RH에서만 관찰되었습니다.

따라서 RH와 LH를 하나의 지도학습 모델에 그대로 넣을 경우 모델이 실제 공정상태가 아니라 Side 정보만으로 불량 여부를 구분하는 Shortcut Learning이 발생할 수 있습니다.

이를 방지하기 위해 최종 지도학습 모델은 **RH 데이터만 사용**하였습니다.

최종 모델은 최근 생산상태로부터 현재 Cycle의 공정값이 얼마나 벗어났는지를 나타내는 **Absolute EWMA5 Feature**와 XGBoost를 사용합니다.

---

# 1. 모델 개요

전체 RG3 데이터:

```text
전체 : 1,182건
RH   : 591건
LH   : 591건
```

전체 불량 25건은 모두 RH에서 발생하였습니다.

최종 학습대상:

```text
RH 전체 : 591건
정상    : 566건
불량    : 25건
```

최종 설정:

| 항목 | 설정 |
|---|---|
| Model | XGBoost |
| 학습 대상 | RH |
| Feature | Absolute EWMA5 |
| Feature 수 | 23개 |
| EWMA Span | 5 |
| Session Gap | 30분 |
| Random State | 42 |
| Validation | Rolling Temporal Validation |
| scale_pos_weight | 22.64 |

---

# 2. 프로젝트 구조

```text
RG3/
│
├─ data/
│  ├─ raw/
│  │  ├─ moldset_labeled_rg3.csv
│  │  ├─ moldset_unlabeled_rg3.csv
│  │  ├─ labeled_data.csv
│  │  └─ unlabeled_data.csv
│  │
│  └─ processed/
│     ├─ train_rg3_preprocessed.csv
│     └─ rg3_model_input.csv
│
├─ src/
│  ├─ preprocess_rg3.py
│  ├─ feature_engineering_rg3.py
│  ├─ train_rg3.py
│  ├─ evaluate_rg3.py
│  ├─ inference_rg3.py
│  └─ config_rg3.py
│
├─ models/
│  └─ rg3_xgb_final.pkl
│
├─ outputs/
│  ├─ rg3_temporal_validation.csv
│  ├─ rg3_holdout_prediction.csv
│  └─ rg3_risk_prediction.csv
│
├─ notebooks/
│  └─ rg3_analysis.ipynb
│
├─ requirements.txt
├─ run_rg3.py
└─ README.md
```

---

# 3. 파일별 역할

| 파일 | 역할 |
|---|---|
| `preprocess_rg3.py` | Train 생산정보 복원, RH 분리, 상수변수 제거, Session 생성 |
| `feature_engineering_rg3.py` | Absolute EWMA5 Feature 생성 |
| `train_rg3.py` | 최종 XGBoost 모델 학습 및 저장 |
| `evaluate_rg3.py` | Rolling Temporal Validation 및 Holdout 평가 |
| `inference_rg3.py` | Test 데이터에 저장 모델을 적용하여 Risk Score 생성 |
| `config_rg3.py` | 경로, Feature, EWMA Span, 모델 Parameter 관리 |
| `run_all.py` | 전처리 → 평가(temporal OOF·metrics) → 학습 → Test 추론 → Cycle 구조진단 |
| `rg3_xgb_final.pkl` | 최종 학습된 XGBoost 모델 |
| `rg3_risk_prediction.csv` | Test 데이터 최종 Risk Ranking 결과 |

---

# 4. 데이터 준비

`data/raw/`에 다음 4개의 파일이 필요합니다.

```text
RG3/data/raw/
├─ moldset_labeled_rg3.csv
├─ moldset_unlabeled_rg3.csv
├─ labeled_data.csv
└─ unlabeled_data.csv
```

Train과 Test는 서로 다른 원본 데이터에서 생산정보를 복원합니다.

## Train

```text
moldset_labeled_rg3.csv
        ↓
labeled_data.csv
        ↓
TimeStamp
PART_NAME
RH_LH
복원
```

## Test

```text
moldset_unlabeled_rg3.csv
        ↓
unlabeled_data.csv
        ↓
TimeStamp
PART_NAME
RH_LH
복원
```

Test 추론에서는 정답 Label을 사용하지 않습니다.

---

# 5. 실행환경 구성

공식 재현환경은 Linux + Python 3.13.5입니다. RG3 프로젝트 폴더로 이동합니다.

```bash
cd RG3  # final 폴더에서 실행
```

가상환경 생성 및 활성화:

```bash
uv venv --python 3.13.5
source .venv/bin/activate
```

고정 버전 설치:

```bash
python -m pip install -r requirements.lock.txt
```

Windows 및 다른 Python 환경에서는 XGBoost의 산출값이 달라질 수 있으므로 공식 수치 재현에는 위 환경을 사용합니다.

---

# 6. 전체 Pipeline 실행

다음 명령어 하나로 전체 과정을 실행합니다.

```powershell
python run_all.py
```

실행순서:

```text
[1/5] Preprocess
        ↓
moldset_labeled_rg3.csv 로드
        ↓
labeled_data.csv에서 생산정보 복원
        ↓
RH 591건 추출
        ↓
상수변수 제거
        ↓
30분 기준 Session 생성


[2/5] Feature Engineering
        ↓
Absolute EWMA5
23개 Feature 생성


[3/5] Temporal / Holdout Evaluation
        ↓
Rolling Temporal Validation
        ↓
Initial Holdout 평가


[4/5] Final Model Training
        ↓
전체 RH 591건으로
XGBoost 재학습
        ↓
models/rg3_xgb_final.pkl 저장


[5/5] Test Inference
        ↓
moldset_unlabeled_rg3.csv 로드
        ↓
unlabeled_data.csv에서
생산정보 복원
        ↓
RH 제품 추론
        ↓
Risk Score / Risk Rank 생성
        ↓
outputs/rg3_risk_prediction.csv 저장
```

---

# 7. Train 전처리

학습 데이터는 다음 과정을 거칩니다.

```text
moldset_labeled_rg3.csv
        ↓
labeled_data.csv와 연결
        ↓
TimeStamp / PART_NAME / RH_LH 복원
        ↓
RH만 추출
        ↓
Clamp_Open_Position 제거
        ↓
TimeStamp 기준 정렬
        ↓
30분 이상 생산공백 기준
Session 생성
```

최종 RH 데이터:

```text
Rows   : 591
Normal : 566
Defect : 25
```

---

# 8. Absolute EWMA5

RG3의 핵심 Feature입니다.

단순히 현재 센서값이 높은지 낮은지를 보는 대신:

```text
현재 공정값이
최근 생산상태로부터
얼마나 크게 벗어났는가?
```

를 계산합니다.

개념적인 계산방법:

```python
past_ewma = (
    x.shift(1)
     .ewm(
         span=5,
         adjust=False,
     )
     .mean()
)

abs_ewma5 = abs(
    current_value
    - past_ewma
)
```

`shift(1)`을 먼저 적용하여 현재 Cycle의 값이 자신의 EWMA 기준값 계산에 포함되지 않도록 합니다.

EWMA는 동일 Session 내부에서만 계산합니다.

최종적으로 23개 센서에 대해:

```text
Absolute EWMA5 Feature 23개
```

를 생성합니다.

---

# 9. Feature 선정 결과

Repeated CV 기준:

```text
Original Feature
PR-AUC = 0.1121

Absolute EWMA5
PR-AUC = 0.2047
```

약 82.6% 개선되었습니다.

미래 Session 검증:

```text
Original
PR-AUC = 0.0381

Original + Abs EWMA5
PR-AUC = 0.2330

Abs EWMA5 Only
PR-AUC = 0.3136
```

따라서 최종 모델에서는 Original Feature와 혼합하지 않고 **Absolute EWMA5 23개만 사용**합니다.

---

# 10. XGBoost 설정

최종 모델 Parameter:

```python
n_estimators = 300
max_depth = 3
learning_rate = 0.03
subsample = 0.8
colsample_bytree = 0.8
eval_metric = "logloss"
random_state = 42
```

클래스 불균형은 다음 방식으로 반영합니다.

```python
scale_pos_weight = (
    normal_count
    / defect_count
)
```

최종 전체 RH 학습에서는:

```text
566 / 25
= 22.64
```

입니다.

---

# 11. Validation

RG3는 Random Split 성능보다 실제 미래 생산환경으로의 일반화 성능을 중요하게 평가하였습니다.

최종 검증에는 Rolling Temporal Validation을 사용합니다.

```text
Fold 1
Train      : Session 1~2
Validation : Session 3

Fold 2
Train      : Session 1~3
Validation : Session 4

Fold 3
Train      : Session 1~4
Validation : Session 5
```

실제 재현 결과:

| Fold | PR-AUC | PR Lift | ROC-AUC |
|---|---:|---:|---:|
| S1~2 → S3 | 0.3136 | 6.1781 | 0.6642 |
| S1~3 → S4 | 0.0465 | 0.8602 | 0.2964 |
| S1~4 → S5 | 0.0961 | 2.8191 | 0.7520 |

---

# 12. Initial Holdout

초기 Holdout은 다음과 같이 구성하였습니다.

```text
Train
Session 1~3

Test
Session 4~5
```

결과:

```text
Defect Rate : 0.0400
PR-AUC      : 0.0415
PR Lift     : 1.0375
ROC-AUC     : 0.4254
```

Session별 성능변동이 크게 나타났기 때문에 RG3 모델은 고정 Threshold를 이용한 자동 정상/불량 판정기로 사용하지 않습니다.

---

# 13. 최종 모델 저장

검증 완료 후 전체 RH 591건으로 XGBoost를 다시 학습합니다.

실제 최종 학습 결과:

```text
Rows             : 591
Normal           : 566
Defect           : 25
scale_pos_weight : 22.6400
Features         : 23
```

저장 위치:

```text
models/rg3_xgb_final.pkl
```

---

# 14. Test 데이터 추론

전체 Pipeline을 실행하면 Test 추론까지 자동으로 수행됩니다.

```powershell
python run_all.py
```

이미 모델 학습이 완료되어 Test만 다시 실행하고 싶다면:

```powershell
python -m src.inference_rg3
```

사용 파일:

```text
data/raw/moldset_unlabeled_rg3.csv
data/raw/unlabeled_data.csv
models/rg3_xgb_final.pkl
```

---

# 15. Test 추론 과정

```text
moldset_unlabeled_rg3.csv
        ↓
unlabeled_data.csv와 연결
        ↓
original_index
TimeStamp
PART_NAME
RH_LH
복원
        ↓
RH / LH 분리
        ↓
RH 생산 Session 생성
        ↓
Absolute EWMA5 생성
        ↓
rg3_xgb_final.pkl 로드
        ↓
Risk Score 계산
        ↓
Risk Rank 계산
        ↓
rg3_risk_prediction.csv 저장
```

---

# 16. Test 결과 파일

최종 Test 추론 결과:

```text
outputs/rg3_risk_prediction.csv
```

주요 컬럼:

| 컬럼 | 의미 |
|---|---|
| `original_index` | 원본 데이터 행 위치 |
| `TimeStamp` | 생산시간 |
| `PART_NAME` | 제품/금형 정보 |
| `RH_LH` | RH/LH 구분 |
| `Session` | 생산 Session |
| `Risk_Score` | 모델의 불량 위험도 |
| `Risk_Rank` | RH 데이터 내 위험도 순위 |
| `Inspection_Priority` | 검사 우선순위 |
| `AI_Status` | AI 적용상태 |

---

# 17. RH 처리

RH 제품에는 저장된 XGBoost 모델을 적용합니다.

```text
RH
↓
Absolute EWMA5
↓
XGBoost
↓
Risk Score
↓
Risk Rank
```

기본적으로 검증되지 않은 고정 Threshold를 적용하지 않고 Risk Ranking을 제공합니다.

```text
AI_Status
= RH_RISK_RANKING

Inspection_Priority
= RANK_BY_RISK_SCORE
```

---

# 18. LH 처리

학습데이터에서 LH 불량사례가 존재하지 않았기 때문에 LH 제품에 대해 AI 자동 정상/불량 판정을 수행하지 않습니다.

```text
AI_Status
= LH_EXCLUDED_NO_DEFECT_TRAINING

Inspection_Priority
= EXISTING_INSPECTION
```

즉 LH는 기존 품질검사를 유지합니다.

---

# 19. 모델 활용 방식

RG3는 자동 합격/불합격 판정기가 아닙니다.

```text
Risk Score 높음
→ 상대적으로 우선검사가 필요한 제품

Risk Score 낮음
→ 정상 확정 아님
```

일부 실제 불량이 Risk Ranking 하위에 위치하는 Hard Defect 사례가 존재하기 때문에 낮은 Risk Score만으로 검사를 생략해서는 안 됩니다.

---

# 20. 운영 시 주의사항

- RG3는 생산 Session별 성능변동이 큽니다.
- Random CV만으로 미래 성능을 판단하면 안 됩니다.
- 새로운 생산 Session에서 데이터 분포가 크게 변할 수 있습니다.
- 낮은 Risk Score를 자동 정상판정으로 사용하지 않습니다.
- LH에는 검증 가능한 불량 학습사례가 없으므로 기존 검사를 유지합니다.
- EWMA Feature 생성 시 생산시간 순서를 임의로 섞으면 안 됩니다.
- Test에서는 정답 Label을 사용하지 않습니다.
- Test 메타정보는 반드시 `unlabeled_data.csv`에서 복원합니다.
- `.pkl` 모델과 Feature Engineering 코드를 함께 관리해야 동일한 추론을 재현할 수 있습니다.

---

# 21. 핵심 실행 명령어

전체 학습 + 검증 + 모델 저장 + Test:

```bash
cd RG3  # final 폴더에서 실행
source .venv/bin/activate
python run_all.py
```

Test만 다시 실행:

```powershell
python -m src.inference_rg3
```

---

# 22. 핵심 요약

```text
RG3
=
RH 전용 모델
+
Absolute EWMA5
+
XGBoost
+
Rolling Temporal Validation
+
Risk Ranking

목적
=
자동 정상/불량 판정이 아니라

최근 생산상태와 비교하여
공정이 상대적으로 크게 이탈한 제품을
우선적으로 검사하기 위한
제조 품질 의사결정 지원 모델
```

## 2026-10-08 재현성 검증 안내
- Linux Python 3.13.5에서 `requirements.lock.txt`의 고정 버전으로 `python run_all.py`를 반복 검증했으며 공식 CSV·보고서 수치와 일치함.
- Windows 및 다른 Python 환경에서는 비트 단위 일치를 보장하지 않음.

- 전체 실행: `python run_all.py` (사후 Cycle 분석 포함). `OUTPUT_MANIFEST.md` 확인.


## 최종 제출 기준 (2026-10-08 재실행)

공식 재현 진입점은 **`python run_all.py`** 하나입니다. `run_rg3.py`는 내부 기본 실행기로 사용합니다.
전처리 후 `outputs/rg3_temporal_validation.csv`, `rg3_oof_prediction.csv`(시간순 Fold 1~3 검증 예측 447건),
`rg3_holdout_prediction.csv`, `rg3_metrics.csv`, `rg3_cycle_*`, `rg3_risk_prediction.csv`와
`rg3_inference_result.csv`를 모두 생성합니다. Cycle 결과는 사후 구조진단이며 정식 RH Holdout 대체가 아닙니다.

최종 검증 표는 이번 재실행 성능을 기준으로 통일했습니다. 단, 초기 후보 탐색 결과는 별도 조건의 실험값으로 구분합니다.
공식 제출 성능은 본 ZIP의 `outputs/rg3_metrics.csv`와 재실행 결과를 우선합니다.
환경 버전은 `requirements.lock.txt`를 참조하세요. 다른 OS/Python 버전에서 비트 단위 일치를 보장하지 않습니다.


## 실제 검증 기록

- 재실행 환경: Python 3.13.5, NumPy 2.3.5, pandas 2.2.3, scikit-learn 1.8.0, XGBoost 3.1.3, joblib 1.5.3.
- `python run_all.py`로 전체 pipeline(신규 test 위험순위까지)을 실행했고, 이어 `python run_all.py --skip-test`에서 metric CSV가 동일함을 확인함.
- 공식 수치: Rolling PR-AUC 0.313587 / 0.046489 / 0.096094; Final Holdout PR-AUC 0.041461, ROC-AUC 0.425417; Cycle post-hoc PR-AUC 0.412428.
- OOF 파일은 **3개 시간검증 Fold의 447개 검증 예측**이며 591개 행 전체 OOF가 아님.
- 공식 unlabeled Test 예측 행수는 35,941, 정답 라벨이 없어 성능지표를 산출하지 않음.
- RG3에는 독립적 자동 Drift Detector가 없음. Session/공정분포 감시는 **현장 운영 제안**이며 구현 기능으로 기술하지 않음.
- 노트북의 저장된 오류 출력을 정리했으나 노트북 전체를 깨끗한 커널에서 순서대로 재실행한 것은 아님. Python 실행 스크립트를 재현 정본으로 사용.
