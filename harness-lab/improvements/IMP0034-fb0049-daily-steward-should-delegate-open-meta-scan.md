---
id: IMP0034
record_type: improvement_dossier
created_at: '2026-05-17T09:44:51+09:00'
updated_at: '2026-05-17T09:45:31+09:00'
status: adopted
source_type: observation
scope: harnessops-core
maturity: adopted
relation: new
promotion_level: target-lab-case
source_feedback: FB0049
eval_cases:
- E0038
hypotheses:
- H0038
decisions:
- D0039
research_scans: []
classification:
  capability: daily_steward_orchestration
  failure_class: nested_open_scan_not_delegated
guard:
  status: implemented
  path: tests/test_cli/test_steward.py::test_steward_preflight_json_reports_run_ledger
investigation: []
links:
  issue_url:
---

# IMP0034: FB0049: Daily steward should delegate open meta scan

## Status

- status: adopted
- maturity: adopted
- source_type: observation
- scope: harnessops-core
- relation: new
- promotion_level: target-lab-case
- source_feedback: `FB0049`
- linked_records: `FB0049`, `E0038`, `H0038`, `D0039`

## Source Observation

Source: `harness-lab/records/feedback/FB0049-daily-steward-should-delegate-open-meta-scan.md`

# FB0049: Daily steward should delegate open meta scan

## 概要

Daily steward supervisor currently lists invention as one lane; hops-open-meta-scan is only nested inside invention guidance, so the supervisor does not spawn a dedicated open-meta-scan subagent or make its raw ideas an explicit handoff into routing and priority work.

## 再現

Run hops steward preflight --json and inspect supervisor_plan.lanes: hops-open-meta-scan is not a lane even though hops-invention-steward mentions it.

## 期待する上流変更

Add an explicit open-meta-scan supervisor lane using hops-open-meta-scan, then make invention review the raw ideas and record selected candidates so priority-improvement-steward can pick them up.

## Target Capability

- capability: daily_steward_orchestration
- failure_class: nested_open_scan_not_delegated

## Investigation

調査メモはまだありません。

## Research Scans

research scan はまだありません。


## Evaluation

### E0038: E0038: FB0049-daily-steward-should-delegate-open-meta-scan を評価


- source: `harness-lab/records/eval-cases/E0038-fb0049-daily-steward-should-delegate-open-meta-scan.md`

- capability: daily_steward_orchestration

- failure_class: nested_open_scan_not_delegated

- manual_eval_yml: `harness-lab/views/eval-results/E0038-manual-score.yml`
- manual_eval_md: `harness-lab/views/eval-results/E0038-manual-score.md`
- scores: impact=4, mechanism_clarity=5, evaluability=5, minimality=5, regression_risk=1, operator_burden=2, anti_theater=5, maintainability=4, privacy_sanitization_risk=0
- notes: Preflight JSON now shows hops-open-meta-scan as supervisor lane order 3 and subagent_plan recommends open-meta-scan. Invention skill now reviews prior raw ideas and records selected candidates for priority-improvement. Focused tests and ruff passed.


## Hypotheses

### H0038: H0038: E0038-fb0049-daily-steward-should-delegate-open-meta-scan の仮説


Source: `harness-lab/records/hypotheses/H0038-e0038-fb0049-daily-steward-should-delegate-open-meta-scan.md`


# H0038: E0038-fb0049-daily-steward-should-delegate-open-meta-scan の仮説

## 仮説

Daily steward will preserve divergent meta discovery better if open-meta-scan is an explicit supervisor lane before invention.

## メカニズム

Add hops-open-meta-scan to supervisor_plan.lanes so the daily supervisor spawns a dedicated subagent, then make invention review that prior lane's raw ideas and record selected candidates for priority-improvement.

## 最小実装

Insert the open-meta-scan lane, update steward tests, and update repo-local/packaged lane skills plus docs to describe the raw-idea handoff.

## 代替案: 削除または統合

Keep open-meta-scan nested inside hops-invention-steward and rely on that lane to remember to run it.

## 期待される利点

Raw ideas become visible in the steward ledger, invention has an explicit review input, and priority-improvement receives recorded candidates instead of ad hoc summaries.

## 想定される欠点

One more daily steward subagent lane adds latency and one more ledger result to record.

## 評価計画

Check steward preflight JSON includes hops-open-meta-scan at order 3, subagent recommendations include open-meta-scan, packaged skill copies match, and focused steward/contract tests pass.

## 中止基準

Reject if the new lane blocks clean runs, records raw ideas directly without review, or lets priority-improvement depend on unreviewed raw text.


## Evidence

`harness-lab/views/eval-results/E0038-manual-score.md`

## Guard

- status: implemented
- path: tests/test_cli/test_steward.py::test_steward_preflight_json_reports_run_ledger

## Links

- issue_url: 未設定

## Open Questions And Next Action

次の実装または評価ステップは、この dossier と紐づく正規化レコードを更新してから再生成してください。

## Decision Log

### D0039: D0039: adopted H0038


Source: `harness-lab/records/decisions/D0039-adopted-h0038.md`


# D0039: adopted H0038

## 判断

adopted

## 理由

The explicit lane makes open meta scanning a first-class subagent result instead of hidden work inside invention.

## 証拠

hops steward preflight --json includes hops-open-meta-scan at order 3; subagent_plan recommends open-meta-scan; focused steward and contract tests pass; ruff passes.

## 回帰リスク

Low: lane count changes from five to six, so existing consumers expecting five lanes must use supervisor_plan dynamically.

## フォローアップ

Watch the next daily steward run for raw idea quality and whether invention records too many candidates.

## 回帰ガード

tests/test_cli/test_steward.py::test_steward_preflight_json_reports_run_ledger
