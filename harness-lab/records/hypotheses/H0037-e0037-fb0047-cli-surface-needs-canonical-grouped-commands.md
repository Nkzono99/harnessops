---
id: H0037
record_type: hypothesis
created_at: '2026-05-17T04:18:46+09:00'
status: proposed
target_capability: cli_ergonomics
source_eval_case: E0037
---

# H0037: E0037-fb0047-cli-surface-needs-canonical-grouped-commands の仮説

## 仮説

Canonical grouped lab commands reduce automation ambiguity when old entrypoints remain hidden compatibility aliases with warnings and generated next_command strings prefer the grouped forms.

## メカニズム

Keep old Typer commands as hidden aliases that call warn_if_deprecated, route user-facing help/docs/generated queue next commands through grouped command names, and add regression coverage for eval-case/review/memory aliases plus research-scan queue recommendations.

## 最小実装

Audit src/harnessops/cli/lab.py and lab_usage next_command generation for stale command strings; update generated recommendations to hops lab eval-case create, hops lab review queue/context/lint, and hops lab memory compact/prepare; extend tests/test_cli/test_deprecations.py and queue tests to assert canonical output.

## 代替案: 削除または統合

Remove legacy aliases entirely after a migration, but this would break existing automation without evidence that all target repos have migrated.

## 期待される利点

Daily steward lanes can follow queue output without translating stale commands, and new users see one canonical command tree in help/docs.

## 想定される欠点

More alias tests can overfit current command names, so assertions should focus on user-visible help, warnings, and queue next_command strings.

## 評価計画

Run hops lab eval --case E0037 --manual after implementing the audit; focused checks should include tests/test_cli/test_deprecations.py and any lab review queue tests plus doctor/migrate.

## 中止基準

Reject or narrow if CLI audit finds no stale user-facing command strings beyond already-covered aliases, or if maintaining aliases creates more code than consolidating the command registration.
