---
id: IMP0030
record_type: improvement_dossier
created_at: '2026-05-14T01:30:13+09:00'
updated_at: '2026-05-14T01:30:26+09:00'
status: adopted
source_type: friction
scope: harnessops-core
maturity: adopted
relation: extends
promotion_level: shipped-behavior
source_feedback: FB0028
eval_cases:
- E0033
hypotheses:
- H0033
decisions:
- D0034
research_scans: []
classification:
  capability: uvx_update_guidance
  failure_class: stale_hops_update_path
guard:
  status: implemented
  path: tests/test_cli/test_mvp_flow.py::test_hops_usage_notices_stale_harnessops_lock_once; tests/test_cli/test_mvp_flow.py::test_hops_usage_notices_when_current_runtime_is_behind_pypi; tests/test_cli/test_mvp_flow.py::test_update_notice_handles_unreleased_runtime_ahead_of_pypi; tests/test_cli/test_mvp_flow.py::test_update_notice_warns_when_repo_lock_is_newer_than_runtime
investigation: []
links:
  issue_url:
---

# IMP0030: FB0028: Make update notices guide uvx-based HarnessOps upgrades

## Status

- status: adopted
- maturity: adopted
- source_type: friction
- scope: harnessops-core
- relation: extends
- promotion_level: shipped-behavior
- source_feedback: `FB0028`
- linked_records: `FB0028`, `E0033`, `H0033`, `D0034`

## Source Observation

Source: `harness-lab/records/feedback/FB0028-make-update-notices-guide-uvx-based-harnessops-upgrades.md`

# FB0028: Make update notices guide uvx-based HarnessOps upgrades

## 概要

Target and project repositories need a single update path when repo-managed HarnessOps artifacts, the currently running hops runtime, and the latest PyPI release differ. The existing notice only compares the repo lock with the current runtime and still points agents at the hops-update-harness skill or bare hops command.

## 再現

ローカル改善作業中に観測。

## 期待する上流変更

Update the CLI notice so ordinary hops usage in linked repos compares recorded, current, and latest PyPI HarnessOps versions when available, emits uvx --refresh-package harnessops --from harnessops hops update-harness guidance, and keeps migration application behind an explicit follow-up check.

## Target Capability

- capability: uvx_update_guidance
- failure_class: stale_hops_update_path

## Investigation

調査メモはまだありません。

## Research Scans

research scan はまだありません。


## Evaluation

### E0033: E0033: FB0028-make-update-notices-guide-uvx-based-harnessops-upgrades を評価


- source: `harness-lab/records/eval-cases/E0033-fb0028-make-update-notices-guide-uvx-based-harnessops-upgrades.md`

- capability: uvx_update_guidance

- failure_class: stale_hops_update_path

- manual_eval_yml: `harness-lab/views/eval-results/E0033-manual-score.yml`
- manual_eval_md: `harness-lab/views/eval-results/E0033-manual-score.md`
- scores: impact=3, mechanism_clarity=5, evaluability=5, minimality=5, regression_risk=1, operator_burden=0, anti_theater=5, maintainability=4, privacy_sanitization_risk=0
- notes: Existing behavior satisfies FB0028: update_notice.py compares repo-managed, current runtime, and latest PyPI versions; CLI spec documents uvx update-harness, plan-upgrade, doctor, and migrate-check guidance; targeted guard passed with uv run pytest tests/test_cli/test_mvp_flow.py -k update_notice -q (6 passed, 36 deselected). Full steward validation will be run before adoption/finalize.


## Hypotheses

### H0033: H0033: E0033-fb0028-make-update-notices-guide-uvx-based-harnessops-upgrades の仮説


Source: `harness-lab/records/hypotheses/H0033-e0033-fb0028-make-update-notices-guide-uvx-based-harnessops-upgrades.md`


# H0033: E0033-fb0028-make-update-notices-guide-uvx-based-harnessops-upgrades の仮説

## 仮説

Existing update-notice behavior resolves FB0028 by comparing repo-managed, current runtime, and latest PyPI versions, then routing ordinary CLI users to uvx update-harness guidance without auto-applying migrations.

## メカニズム

The CLI computes recorded/current/latest version drift, emits uvx refresh-package update-harness plus plan-upgrade, doctor, and migrate-check commands, caches notices to avoid noise, and leaves migration application explicit.

## 最小実装

No implementation change in this run; reconcile the already-present update_notice.py behavior, CLI spec text, and update_notice regression tests into lab E/H/D records.

## 代替案: 削除または統合

Park FB0028 as duplicate of IMP0017 or IMP0026; rejected because the feedback remains triaged and unlinked even though the behavior now has concrete guards.

## 期待される利点

Closes stale intake and makes the uvx update notice contract traceable to tests, spec, and a guard path.

## 想定される欠点

Medium duplicate risk with IMP0017 and IMP0026, mitigated by classifying this as an extension/resolved-by backfill rather than new feature work.

## 評価計画

Run pytest tests/test_cli/test_mvp_flow.py -k update_notice, then full pytest, ruff, doctor --check-overlay --check-records, and migrate --check before finalizing.

## 中止基準

Reject or reopen if update_notice no longer compares recorded/current/latest versions, stops emitting uvx update-harness guidance, auto-applies migrations, or fails the update_notice guard tests.


## Evidence

`harness-lab/views/eval-results/E0033-manual-score.md`

## Guard

- status: implemented
- path: tests/test_cli/test_mvp_flow.py::test_hops_usage_notices_stale_harnessops_lock_once; tests/test_cli/test_mvp_flow.py::test_hops_usage_notices_when_current_runtime_is_behind_pypi; tests/test_cli/test_mvp_flow.py::test_update_notice_handles_unreleased_runtime_ahead_of_pypi; tests/test_cli/test_mvp_flow.py::test_update_notice_warns_when_repo_lock_is_newer_than_runtime

## Links

- issue_url: 未設定

## Open Questions And Next Action

次の実装または評価ステップは、この dossier と紐づく正規化レコードを更新してから再生成してください。

## Decision Log

### D0034: D0034: adopted H0033


Source: `harness-lab/records/decisions/D0034-adopted-h0033.md`


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
