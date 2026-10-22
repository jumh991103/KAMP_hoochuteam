# KAMP 후추팀 — CN7·RG3 사출성형 품질위험 예측

제6회 K-인공지능 제조데이터 분석 경진대회 후추팀 제출물입니다.

| 경로 | 내용 |
|---|---|
| `소스코드_후추팀/` | 소스코드 (실행 방법은 [소스코드_후추팀/README.md](소스코드_후추팀/README.md) 참고) |
| `결과보고서_후추팀.pdf`, `[후추팀] 제조데이터분석 경진대회 보고서-사출성형.hwpx` | 결과 보고서 |
| `발표자료_후추팀.pdf`, `발표자료_후추팀.pptx` | 발표 자료 |

## 원본 데이터 받기

원본 데이터는 용량 문제(GitHub 파일당 100MB 제한)로 이 저장소에 포함하지 않았습니다.
데이터는 **KAMP(인공지능 중소벤처 제조 플랫폼)** 에서 제공하는 사출성형 제조데이터입니다.

- KAMP: https://www.kamp-ai.kr (회원가입 및 로그인 후 데이터셋 메뉴에서 다운로드)

내려받은 파일은 아래 위치에 두면 코드가 그대로 동작합니다.

```text
소스코드_후추팀/
├─ CN7/data/raw/
│  ├─ labeled_data.csv
│  ├─ moldset_labeled_cn7.csv
│  ├─ moldset_unlabeled_cn7.csv
│  └─ unlabeled_data.csv
└─ RG3/data/raw/
   ├─ labeled_data.csv
   ├─ moldset_labeled_rg3.csv
   ├─ moldset_unlabeled_rg3.csv
   └─ unlabeled_data.csv
```

`labeled_data.csv`와 `unlabeled_data.csv`는 CN7·RG3 폴더에 같은 파일을 넣으면 됩니다.
전처리 결과(`data/processed/`)와 모델 출력(`outputs/`)은 저장소에 포함되어 있습니다.
