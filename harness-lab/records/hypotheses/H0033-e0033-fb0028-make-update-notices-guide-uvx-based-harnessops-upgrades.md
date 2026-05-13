---
id: H0033
record_type: hypothesis
created_at: '2026-05-14T01:27:50+09:00'
status: proposed
target_capability: uvx_update_guidance
source_eval_case: E0033
---

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
