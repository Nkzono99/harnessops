---
id: IMP0033
record_type: improvement_dossier
created_at: '2026-05-17T04:14:55+09:00'
updated_at: '2026-05-17T04:21:50+09:00'
status: parked
source_type: observation
scope: harnessops-core
maturity: investigated
relation: extends
promotion_level: target-lab-case
source_feedback: FB0047
eval_cases:
- E0037
hypotheses:
- H0037
decisions:
- D0038
research_scans: []
classification:
  capability: cli_ergonomics
  failure_class: command_surface_sprawl
guard:
  status: not-defined
  path:
investigation:
- created_at: '2026-05-17T04:15:25+09:00'
  kind: codebase
  summary: 'Open invention scan found command-surface drift beyond the original feedback: current docs/SPEC/tests prefer grouped commands such as hops lab eval-case create and hops lab review queue, while existing research-scan candidates still surface deprecated or stale next commands such as hops lab new-eval-case through review queue output. Treat this as evidence for canonical command aliases plus record/queue migration guidance, not a new isolated feature.'
  evidence_ref: SPEC.md; docs/agent-user-guide.md; tests/test_cli/test_deprecations.py; harness-lab/records/research-scans/RS0001-structure-meta-improvement-research-scan-outputs.md
links:
  issue_url:
---

# IMP0033: FB0047: CLI surface needs canonical grouped commands

## Status

- status: parked
- maturity: investigated
- source_type: observation
- scope: harnessops-core
- relation: extends
- promotion_level: target-lab-case
- source_feedback: `FB0047`
- linked_records: `FB0047`, `E0037`, `H0037`, `D0038`

## Source Observation

Source: `harness-lab/records/feedback/FB0047-cli-surface-needs-canonical-grouped-commands.md`

# FB0047: CLI surface needs canonical grouped commands

## 概要

HarnessOps CLI now exposes several lifecycle actions as top-level or parallel lab commands, making the recommended path harder to learn and increasing automation ambiguity.

## 再現

ローカル改善作業中に観測。

## 期待する上流変更

Group feedback actions under feedback, lab evaluation actions under lab, review actions under lab review, memory compaction under lab memory, and emit deprecation warnings from old entrypoints.

## Target Capability

- capability: cli_ergonomics
- failure_class: command_surface_sprawl

## Investigation

- 2026-05-17T04:15:25+09:00 [codebase] Open invention scan found command-surface drift beyond the original feedback: current docs/SPEC/tests prefer grouped commands such as hops lab eval-case create and hops lab review queue, while existing research-scan candidates still surface deprecated or stale next commands such as hops lab new-eval-case through review queue output. Treat this as evidence for canonical command aliases plus record/queue migration guidance, not a new isolated feature. (evidence: SPEC.md; docs/agent-user-guide.md; tests/test_cli/test_deprecations.py; harness-lab/records/research-scans/RS0001-structure-meta-improvement-research-scan-outputs.md)

## Research Scans

research scan はまだありません。


## Evaluation

### E0037: E0037: FB0047-cli-surface-needs-canonical-grouped-commands を評価


- source: `harness-lab/records/eval-cases/E0037-fb0047-cli-surface-needs-canonical-grouped-commands.md`

- capability: cli_ergonomics

- failure_class: command_surface_sprawl

- manual_eval_yml: `harness-lab/views/eval-results/E0037-manual-score.yml`
- manual_eval_md: `harness-lab/views/eval-results/E0037-manual-score.md`
- scores: impact=3, mechanism_clarity=4, evaluability=4, minimality=4, regression_risk=3, operator_burden=4, anti_theater=4, maintainability=3, privacy_sanitization_risk=5
- notes: Implemented read-time canonicalization for research-scan queue next_command values and added regression coverage in tests/test_cli/test_lab_usage.py; focused pytest passed. This validates the stale queue-command part of FB0047, but not the full command-surface audit for all aliases.


## Hypotheses

### H0037: H0037: E0037-fb0047-cli-surface-needs-canonical-grouped-commands の仮説


Source: `harness-lab/records/hypotheses/H0037-e0037-fb0047-cli-surface-needs-canonical-grouped-commands.md`


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


## Evidence

`harness-lab/views/eval-results/E0037-manual-score.md`

## Guard

- status: not-defined
- path: None

## Links

- issue_url: 未設定

## Open Questions And Next Action

次の実装または評価ステップは、この dossier と紐づく正規化レコードを更新してから再生成してください。

## Decision Log

### D0038: D0038: parked H0037


Source: `harness-lab/records/decisions/D0038-parked-h0037.md`


# D0038: parked H0037

## 判断

parked

## 理由

Queue-time canonicalization is validated and kept as a partial implementation, but the broader CLI surface audit remains incomplete.

## 証拠

E0037 manual eval recorded after implementing _canonical_next_command for research-scan queue output and adding focused regression coverage; uv run pytest tests/test_cli/test_lab_usage.py tests/test_cli/test_deprecations.py passed.

## 回帰リスク

Low for queue output because stored records are unchanged; medium for future alias changes if replacement coverage drifts.

## フォローアップ

Complete the broader FB0047 audit for lab memory/review/eval aliases and generated recommendations, then decide whether to adopt the full hypothesis with a guard.

## 回帰ガード

tests/test_cli/test_lab_usage.py::test_lab_queue_ranks_recorded_work
