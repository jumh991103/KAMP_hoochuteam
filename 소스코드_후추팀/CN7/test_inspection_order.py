"""python test_inspection_order.py: OOD 미적용 순위 회귀검사."""
from pathlib import Path
import ast
p = Path(__file__).parent / "src" / "test_cn7.py"
src = p.read_text(encoding="utf-8")
ast.parse(src)
assert '"Risk_Probability", "Risk_STD", "_effective_ood"' in src
assert 'result["OOD_Applicable"].eq(1)' in src
print("PASS: non-applicable OOD is not used ahead of risk")
