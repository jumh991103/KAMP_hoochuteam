"""공식 RG3 전체 파이프라인 진입점. 모든 출력은 현재 코드로 생성합니다."""
import argparse
import subprocess
import sys
from pathlib import Path
import pandas as pd
import shutil

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "outputs"

def main():
    parser = argparse.ArgumentParser(description="RG3 재현: 평가/모델/추론/Cycle")
    parser.add_argument("--skip-test", action="store_true", help="공식 unlabeled 추론 생략")
    args = parser.parse_args()
    core = [sys.executable, "run_rg3.py"]
    if args.skip_test:
        core.append("--skip-test")
    subprocess.run(core, cwd=ROOT, check=True)
    subprocess.run([sys.executable, "run_rg3_cycle_analysis.py"], cwd=ROOT, check=True)
    summary_path = OUT / "rg3_metrics.csv"
    metrics = pd.read_csv(summary_path)
    cyc = pd.read_csv(OUT / "rg3_cycle_oot_metrics.csv").iloc[0]
    extra = pd.DataFrame([{
        "Evaluation": "Posthoc_Cycle_OOT_2020_11_04",
        "Train_Sessions": "2020-10-21~2020-10-23", "Valid_Session": "2020-11-04",
        "PR_AUC": cyc["PR_AUC"], "ROC_AUC": cyc["ROC_AUC"],
        "Defect_Rate": cyc["Prevalence"], "PR_Lift": cyc["PR_Lift"],
    }])
    pd.concat([metrics, extra], ignore_index=True).to_csv(summary_path, index=False)
    src = OUT / "rg3_risk_prediction.csv"
    alias = OUT / "rg3_inference_result.csv"
    if not args.skip_test:
        if not src.exists():
            raise FileNotFoundError(f"추론 산출물 누락: {src}")
        shutil.copyfile(src, alias)
    print("[OK] Official metrics, temporal OOF, holdout, cycle", "and inference" if not args.skip_test else "(inference skipped)")

if __name__ == "__main__":
    main()
