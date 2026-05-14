---
id: IMP0032
record_type: improvement_dossier
created_at: '2026-05-14T11:11:44+09:00'
updated_at: '2026-05-14T11:13:08+09:00'
status: adopted
source_type: github-issue
scope: harnessops-core
maturity: adopted
relation: extends
promotion_level: harnessops-protocol
source_feedback: FB0039
eval_cases:
- E0035
hypotheses:
- H0035
decisions:
- D0036
research_scans: []
classification:
  capability: unclassified
  failure_class: unclassified
guard:
  status: implemented
  path: tests/test_agent_harness_contract.py
investigation: []
links:
  issue_url: https://github.com/Nkzono99/harnessops/issues/18
---

# IMP0032: FB0039: Consolidate repo-local issue triage into HOPS daily steward

## Status

- status: adopted
- maturity: adopted
- source_type: github-issue
- scope: harnessops-core
- relation: extends
- promotion_level: harnessops-protocol
- source_feedback: `FB0039`
- linked_records: `FB0039`, `E0035`, `H0035`, `D0036`

## Source Observation

Source: `harness-lab/records/feedback/FB0039-consolidate-repo-local-issue-triage-into-hops-daily-steward.md`

# FB0039: Consolidate repo-local issue triage into HOPS daily steward

## 概要

GitHub issue: https://github.com/Nkzono99/harnessops/issues/18
author: Nkzono99
labels: なし
created_at: 2026-05-14T02:03:28Z
updated_at: 2026-05-14T02:03:28Z

## Issue本文
## 背景

runops 側にあった repo-local `triage` skill と `runops-issue-triage-and-run` automation prompt を削除し、issue triage / unattended daily loop は HarnessOps 側の `hops-daily-steward` と `hops-issue-triage` に統一する方針にした。

runops 側の `triage` skill が持っていた汎用機能のうち、HarnessOps 側に寄せるべきものをこの issue で追跡したい。

## 移譲したい機能

- open issue を優先度つきで分類する報告形式を持つ
  - 対応推奨 (高)
  - 対応推奨 (中)
  - 保留 / 要議論
  - close 推奨
- spam / malicious / unrelated issue の close 候補判定を明文化する
- issue close は人間または automation prompt の明示権限がある場合だけ行う、という安全ルールを HOPS daily / issue triage 側へ寄せる
- 対応完了時の issue close 作法を HOPS 側に持つ
  - commit message の `Closes #N`
  - 手動 close コメント
  - won't fix コメント
- `gh issue view` / GitHub connector で本文・コメント・ラベル・再現情報を確認し、不足情報を triage 報告に含める

## 完了条件

- `hops-issue-triage` または `hops-daily-steward` の skill / docs が上記の汎用 issue triage 作法をカバーしている
- repo-local な `triage` skill がなくても、target repository の daily run で issue triage の判断と報告が迷子にならない
- remote actions は automation prompt の権限に従う、という境界が明記されている

## 関連

- runops 側では `.agents/skills/triage`, `.claude/skills/triage`, `.codex/automation-prompts/runops-issue-triage-and-run.md` を削除予定
- runops は target repository として HarnessOps の `hops-daily-steward` に寄せる

## 再現

送信元フィードバックバンドルを参照してください。

## 期待する上流変更

送信元フィードバックバンドルを参照してください。

## Target Capability

- capability: unclassified
- failure_class: unclassified

## Investigation

調査メモはまだありません。

## Research Scans

research scan はまだありません。


## Evaluation

### E0035: E0035: FB0039-consolidate-repo-local-issue-triage-into-hops-daily-steward を評価


- source: `harness-lab/records/eval-cases/E0035-fb0039-consolidate-repo-local-issue-triage-into-hops-daily-steward.md`

- capability: unclassified

- failure_class: unclassified

- manual_eval_yml: `harness-lab/views/eval-results/E0035-manual-score.yml`
- manual_eval_md: `harness-lab/views/eval-results/E0035-manual-score.md`
- scores: impact=4, mechanism_clarity=5, evaluability=4, minimality=5, regression_risk=2, operator_burden=2, anti_theater=5, maintainability=5, privacy_sanitization_risk=2
- notes: Updated hops-issue-triage with no-argument open issue discovery, priority buckets, close-candidate heuristics, remote-action authority boundary, and completion close conventions. Daily steward now delegates no-argument open issue discovery to hops-issue-triage. Contract tests, ruff, doctor, and migrate check passed.


## Hypotheses

### H0035: H0035: E0035-fb0039-consolidate-repo-local-issue-triage-into-hops-daily-steward の仮説


Source: `harness-lab/records/hypotheses/H0035-e0035-fb0039-consolidate-repo-local-issue-triage-into-hops-daily-steward.md`


# H0035: E0035-fb0039-consolidate-repo-local-issue-triage-into-hops-daily-steward の仮説

## 仮説

A repo-local issue triage skill can replace target-specific triage prompts when it discovers open issues by default, reports priority/risk/closure recommendations, and routes issue changes through HarnessOps records while honoring explicit remote-action authority.

## メカニズム

Document a no-argument open-issue intake path, priority buckets, spam/unrelated close-candidate heuristics, missing-information checks, and safe close/commit conventions in hops-issue-triage, then expose the same lane expectation from hops-daily-steward.

## 最小実装

Update hops-issue-triage SKILL.md and packaged assets; add contract tests covering no-argument open issue discovery, priority report buckets, close safety, and completion close conventions.

## 代替案: 削除または統合

新しい挙動を追加する前に、既存のルール、プロファイル、スキル、テンプレートを削除、統合、厳格化できないか評価してください。

## 期待される利点

紐づく評価ケース `E0035` が、運用者負担を減らし、プロジェクト固有文脈を上流へ漏らさずに通る。

## 想定される欠点

想定される欠点: ルーティング摩擦、偽陽性、保守負担が増える可能性。採用にはこの点の明示的な確認が必要です。

## 評価計画

`hops eval --case E0035 --manual` を実行し、採用判断を作る前に多軸スコアを記録する。

## 中止基準

紐づく評価ケースを改善しない、プライバシーリスクを増やす、または失敗クラスを減らさずにガバナンス構造だけを追加する場合、この仮説を却下または保留する。


## Evidence

`harness-lab/views/eval-results/E0035-manual-score.md`

## Guard

- status: implemented
- path: tests/test_agent_harness_contract.py

## Links

- issue_url: https://github.com/Nkzono99/harnessops/issues/18

## Open Questions And Next Action

次の実装または評価ステップは、この dossier と紐づく正規化レコードを更新してから再生成してください。

## Decision Log

### D0036: D0036: adopted H0035


Source: `harness-lab/records/decisions/D0036-adopted-h0035.md`


# D0036: adopted H0035

## 判断

adopted

## 理由

The issue triage workflow now covers target-repo open issue intake without relying on repo-local triage skills, while preserving HarnessOps record routing and remote-action authorization boundaries.

## 証拠

Updated hops-issue-triage and hops-daily-steward skills; synchronized packaged Codex/Claude assets; uv run pytest tests/test_agent_harness_contract.py -q; uv run ruff check tests/test_agent_harness_contract.py; hops doctor --check-overlay --check-records; hops migrate --check; manual eval E0035.

## 回帰リスク

Low. The change is skill/documentation guidance and contract tests; risk is over-triaging unrelated issues, mitigated by close-candidate and remote-action authority rules.

## フォローアップ

Consider a future CLI helper that emits the open issue triage report from gh/GitHub connector data.

## 回帰ガード

tests/test_agent_harness_contract.py
