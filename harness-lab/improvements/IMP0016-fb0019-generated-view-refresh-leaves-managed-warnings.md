---
id: IMP0016
record_type: improvement_dossier
created_at: '2026-05-13T11:45:06+09:00'
updated_at: '2026-05-13T11:48:35+09:00'
status: adopted
source_type: research-scan
scope: harnessops-core
maturity: adopted
relation: extends
promotion_level: target-lab-case
source_feedback: FB0019
eval_cases:
- E0019
hypotheses:
- H0019
decisions:
- D0020
research_scans: []
classification:
  capability: generated_view_management
  failure_class: stale_generated_view_repair_gap
guard:
  status: implemented
  path: tests/test_cli/test_mvp_flow.py
investigation:
- created_at: '2026-05-13T11:45:19+09:00'
  kind: codebase
  summary: RS0002 and code inspection show refresh_views only regenerates imported-feedback, improvements, and research-scans for lab overlays, while doctor validates the lock hashes for README, backlog, imported-feedback, improvements, research-scans, and score-trajectory. A temporary-copy reproduction confirmed lab refresh-views leaves README, backlog, and score-trajectory warnings after refreshing dynamic views.
  evidence_ref: RS0002; src/harnessops/core/render.py; src/harnessops/core/validation.py; src/harnessops/core/overlay.py
links:
  issue_url:
---

# IMP0016: FB0019: Generated view refresh leaves managed warnings

## Status

- status: adopted
- maturity: adopted
- source_type: research-scan
- scope: harnessops-core
- relation: extends
- promotion_level: target-lab-case
- source_feedback: `FB0019`
- linked_records: `FB0019`, `E0019`, `H0019`, `D0020`

## Source Observation

Source: `harness-lab/records/feedback/FB0019-generated-view-refresh-leaves-managed-warnings.md`

# FB0019: Generated view refresh leaves managed warnings

## 概要

The current lab refresh-views command refreshes dynamic lab views but leaves some doctor-managed generated artifacts stale, so doctor remains ok with generated-view warnings after the apparent repair command.

## 再現

Run hops doctor --check-overlay --check-records, then hops lab refresh-views, then doctor again; README, backlog, and score-trajectory warnings remain.

## 期待する上流変更

Provide a refresh path that updates every doctor-managed lab generated artifact or clearly reports the next repair action, so operators do not learn to ignore stale generated-view warnings.

## Target Capability

- capability: generated_view_management
- failure_class: stale_generated_view_repair_gap

## Investigation

- 2026-05-13T11:45:19+09:00 [codebase] RS0002 and code inspection show refresh_views only regenerates imported-feedback, improvements, and research-scans for lab overlays, while doctor validates the lock hashes for README, backlog, imported-feedback, improvements, research-scans, and score-trajectory. A temporary-copy reproduction confirmed lab refresh-views leaves README, backlog, and score-trajectory warnings after refreshing dynamic views. (evidence: RS0002; src/harnessops/core/render.py; src/harnessops/core/validation.py; src/harnessops/core/overlay.py)

## Research Scans

research scan はまだありません。


## Evaluation

### E0019: E0019: FB0019-generated-view-refresh-leaves-managed-warnings を評価


- source: `harness-lab/records/eval-cases/E0019-fb0019-generated-view-refresh-leaves-managed-warnings.md`

- capability: generated_view_management

- failure_class: stale_generated_view_repair_gap

- manual_eval_yml: `harness-lab/views/eval-results/E0019-manual-score.yml`
- manual_eval_md: `harness-lab/views/eval-results/E0019-manual-score.md`
- scores: impact=4, mechanism_clarity=5, evaluability=5, minimality=5, regression_risk=2, operator_burden=5, anti_theater=5, maintainability=4, privacy_sanitization_risk=5
- notes: Implemented lab refresh-views so it first refreshes doctor-managed overlay artifacts, then regenerates dynamic lab views with deduplicated output. Focused regression covers stale README/backlog/score-trajectory lock warnings and preserves research-scan view content; doctor now reports ok without generated-view warnings.


## Hypotheses

### H0019: H0019: E0019-fb0019-generated-view-refresh-leaves-managed-warnings の仮説


Source: `harness-lab/records/hypotheses/H0019-e0019-fb0019-generated-view-refresh-leaves-managed-warnings.md`


# H0019: E0019-fb0019-generated-view-refresh-leaves-managed-warnings の仮説

## 仮説

If lab refresh-views regenerates every lab artifact that doctor validates as managed, then operators can clear stale generated-view warnings with the obvious lab repair command instead of learning to ignore warnings.

## メカニズム

doctor warns by comparing lock managed_file hashes. The lab refresh command currently updates only dynamic views and their hashes, leaving static/generated lab artifacts under old hashes. Reusing the managed overlay refresh path, then dynamic view refresh, will align the command with the full managed set.

## 最小実装

Change hops lab refresh-views to refresh managed overlay files for the current lab overlay before regenerating dynamic views, then keep lock hashes current. Add a regression test where README/backlog/score-trajectory are stale and lab refresh-views clears doctor warnings.

## 代替案: 削除または統合

Add a new top-level hops views refresh/status command and leave lab refresh-views as-is, but this adds surface area before the existing command is made honest.

## 期待される利点

A single lab command repairs all doctor-managed generated lab artifacts and reduces warning fatigue.

## 想定される欠点

Refreshing managed files can overwrite generated static text if it is not locally edited; conflict behavior must preserve edited managed files via existing .new behavior.

## 評価計画

In a fixture repo, stale README/backlog/score-trajectory and run hops lab refresh-views; doctor --check-overlay --check-records should produce no generated-view warnings. Existing dynamic view refresh behavior should still include research scans and improvements.

## 中止基準

Reject this path if it overwrites locally edited managed files without a .new conflict copy, or if it requires a broader views command before the lab-specific repair works.


## Evidence

`harness-lab/views/eval-results/E0019-manual-score.md`

## Guard

- status: implemented
- path: tests/test_cli/test_mvp_flow.py

## Links

- issue_url: 未設定

## Open Questions And Next Action

次の実装または評価ステップは、この dossier と紐づく正規化レコードを更新してから再生成してください。

## Decision Log

### D0020: D0020: adopted H0019


Source: `harness-lab/records/decisions/D0020-adopted-h0019.md`


# D0020: adopted H0019

## 判断

adopted

## 理由

H0019 の最小実装を採用。既存の lab refresh-views を広げるだけで、doctor が管理する lab generated artifact の stale warning を同じコマンドで修復できる。

## 証拠

Focused regression test passes; tests/test_cli/test_mvp_flow.py passes; running hops lab refresh-views on this repository clears generated-view warnings from doctor.

## 回帰リスク

Low to moderate: refresh_managed_files may touch generated static lab files, but existing conflict handling writes .new for locally edited managed files and dynamic views are regenerated as before.

## フォローアップ

Consider a future top-level hops views refresh/status alias if generated-view management grows beyond lab-specific usage.

## 回帰ガード

tests/test_cli/test_mvp_flow.py
