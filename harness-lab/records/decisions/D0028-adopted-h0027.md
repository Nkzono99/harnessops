---
id: D0028
record_type: decision
created_at: '2026-05-13T22:11:03+09:00'
status: adopted
source: H0027
evidence:
  summary: pytest -q; ruff check .; hops doctor --check-overlay --check-records; hops migrate --check; focused doctor bridge fallback tests passed.
  guard_path: tests/test_cli/test_mvp_flow.py::test_doctor_warns_about_stale_editable_bridge_fallback
---

# D0028: adopted H0027

## 判断

adopted

## 理由

Adopted because doctor now detects stale editable HarnessOps bridge fallback text in target repos that cannot provide a local hops console script, while leaving generated uvx bridge guidance and local hops providers alone.

## 証拠

pytest -q; ruff check .; hops doctor --check-overlay --check-records; hops migrate --check; focused doctor bridge fallback tests passed.

## 回帰リスク

Low; the change is a warning-only validation hook scoped to repo-local harnessops-bridge skill files and guarded by positive/negative CLI tests.

## フォローアップ

Remote issue #9 remains open because automation was not authorized to comment or close GitHub issues.

## 回帰ガード

tests/test_cli/test_mvp_flow.py::test_doctor_warns_about_stale_editable_bridge_fallback
