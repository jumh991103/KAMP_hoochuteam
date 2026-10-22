from pathlib import Path
from src.cycle_analysis_rg3 import run_cycle_analysis

def main():
    run_cycle_analysis(
        data_path=Path("data/raw/labeled_data.csv"),
        output_dir=Path("outputs"),
    )

if __name__ == "__main__":
    main()
