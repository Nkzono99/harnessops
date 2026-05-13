---
id: D0034
record_type: decision
created_at: '2026-05-14T01:30:04+09:00'
status: adopted
source: H0033
evidence:
  summary: 'uv run pytest tests/test_cli/test_mvp_flow.py -k update_notice -q (6 passed, 36 deselected); uv run pytest -q (94 passed); uv run ruff check src tests (passed); hops doctor --check-overlay --check-records (ok); hops migrate --check (no pending migrations); evidence refs: src/harnessops/cli/update_notice.py, tests/test_cli/test_mvp_flow.py, specs/cli-spec.md, harness-lab/views/eval-results/E0033-manual-score.yml'
  guard_path: tests/test_cli/test_mvp_flow.py::test_hops_usage_notices_stale_harnessops_lock_once; tests/test_cli/test_mvp_flow.py::test_hops_usage_notices_when_current_runtime_is_behind_pypi; tests/test_cli/test_mvp_flow.py::test_update_notice_handles_unreleased_runtime_ahead_of_pypi; tests/test_cli/test_mvp_flow.py::test_update_notice_warns_when_repo_lock_is_newer_than_runtime
---

# D0034: adopted H0033

## 判断

adopted

## 理由

Adopted as a resolved-by-existing-behavior backfill: the update notice now compares repo-managed, current runtime, and latest PyPI versions, emits uvx update-harness guidance, and keeps migrations behind explicit doctor/migrate checks.

## 証拠

uv run pytest tests/test_cli/test_mvp_flow.py -k update_notice -q (6 passed, 36 deselected); uv run pytest -q (94 passed); uv run ruff check src tests (passed); hops doctor --check-overlay --check-records (ok); hops migrate --check (no pending migrations); evidence refs: src/harnessops/cli/update_notice.py, tests/test_cli/test_mvp_flow.py, specs/cli-spec.md, harness-lab/views/eval-results/E0033-manual-score.yml

## 回帰リスク

Low implementation risk because this run does not change code. Medium duplicate-record risk with IMP0017 and IMP0026 is mitigated by treating FB0028 as an extension/resolution backfill instead of a new feature surface.

## フォローアップ

Keep FB0028 linked through the dossier and retain update_notice guard tests; reopen if future releases remove recorded/current/latest comparison, uvx update-harness guidance, or explicit migration checks.

## 回帰ガード

tests/test_cli/test_mvp_flow.py::test_hops_usage_notices_stale_harnessops_lock_once; tests/test_cli/test_mvp_flow.py::test_hops_usage_notices_when_current_runtime_is_behind_pypi; tests/test_cli/test_mvp_flow.py::test_update_notice_handles_unreleased_runtime_ahead_of_pypi; tests/test_cli/test_mvp_flow.py::test_update_notice_warns_when_repo_lock_is_newer_than_runtime
