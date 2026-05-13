---
id: IMP0021
record_type: improvement_dossier
created_at: '2026-05-13T18:30:31+09:00'
updated_at: '2026-05-13T18:30:39+09:00'
status: adopted
source_type: github-issue
scope: harnessops-core
maturity: adopted
relation: extends
promotion_level: harnessops-protocol
source_feedback: FB0024
eval_cases:
- E0024
hypotheses:
- H0024
decisions:
- D0025
research_scans: []
classification:
  capability: unclassified
  failure_class: unclassified
guard:
  status: implemented
  path: tests/test_agent_harness_contract.py
investigation: []
links:
  issue_url: https://github.com/Nkzono99/harnessops/issues/11
---

# IMP0021: FB0024: Make hops-research-improvements less myopic

## Status

- status: adopted
- maturity: adopted
- source_type: github-issue
- scope: harnessops-core
- relation: extends
- promotion_level: harnessops-protocol
- source_feedback: `FB0024`
- linked_records: `FB0024`, `E0024`, `H0024`, `D0025`

## Source Observation

Source: `harness-lab/records/feedback/FB0024-make-hops-research-improvements-less-myopic.md`

# FB0024: Make hops-research-improvements less myopic

## 概要

GitHub issue: https://github.com/Nkzono99/harnessops/issues/11
author: Nkzono99
labels: enhancement
created_at: 2026-05-13T09:17:09Z
updated_at: 2026-05-13T09:17:09Z

## Issue本文
## Problem

The `hops-research-improvements` workflow currently tends to select very local, near-term improvement candidates. In recent target-repo use it quickly promoted concrete friction such as individual CLI traceback handling or update-harness edge cases. Those can be useful, but the workflow is too eager to turn the latest observed annoyance into a lab record or issue.

This makes the skill feel myopic: it captures symptoms before stepping back to ask whether the observation is part of a broader capability gap, a repeated cross-project pattern, or just a small local bug that should be parked.

## Expected behavior

Before creating `hops lab capture`, `research-scan`, or a GitHub issue, the skill should do an explicit strategy pass:

- Group observations by horizon: immediate bugfix, workflow design, evaluation methodology, cross-project harness principle.
- Prefer systemic improvements over one-off local fixes unless the local fix is a guardrail for a broader failure class.
- Require a short generalization check: what capability does this improve, which failure class does it represent, and would it matter in at least two target/project repos?
- Add a "park/reject as local" path for observations that are real but too narrow.
- Encourage synthesis across several small frictions before proposing a new improvement dossier.

## Possible implementation

Update the `hops-research-improvements` skill with a mandatory pre-capture section such as:

1. List candidate observations.
2. Mark each as `local-only`, `repeated-pattern`, `cross-project`, or `strategic`.
3. Choose at most one systemic candidate.
4. Park narrow candidates unless they are evidence for the systemic one.
5. Only then run `hops lab capture`, `hops lab research-scan`, or `hops lab investigate/classify`.

The workflow could also add wording like: "Do not create a new record for the newest friction unless it reveals a broader mechanism or evaluation gap."

## Evaluation idea

Create an eval case with several local frictions, for example:

- a CLI command prints a traceback for invalid input
- update-harness emits a confusing `.new` file
- a target skill lacks context about repo role

The expected output should not be three separate improvement issues. It should synthesize a broader candidate, such as "research-improvement candidate selection needs a horizon/generalization guard", and park the narrow fixes as evidence.

## Acceptance criteria

- The skill contains an explicit anti-myopia / horizon-scan step before capture or issue creation.
- The output format includes a `park` or `local-only` recommendation path.
- A test or fixture verifies that multiple narrow observations are synthesized into one broader improvement instead of being promoted independently.
- Existing useful behavior remains: truly urgent guardrail bugs can still be captured when they protect a wider failure class.

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

### E0024: E0024: FB0024-make-hops-research-improvements-less-myopic を評価


- source: `harness-lab/records/eval-cases/E0024-fb0024-make-hops-research-improvements-less-myopic.md`

- capability: unclassified

- failure_class: unclassified

- manual_eval_yml: `harness-lab/views/eval-results/E0024-manual-score.yml`
- manual_eval_md: `harness-lab/views/eval-results/E0024-manual-score.md`
- scores: impact=4, mechanism_clarity=5, evaluability=5, minimality=5, regression_risk=1, operator_burden=2, anti_theater=5, maintainability=5, privacy_sanitization_risk=1
- notes: Implemented the anti-myopia gate directly in the hops-research-improvements skill: it now requires horizon/generalization classification before capture or issue creation, parks local-only frictions, limits promotion to one systemic candidate, and includes a concrete synthesis example. Packaged Codex/Claude copies stay equal to the repo-local skill and contract tests assert the new fixture terms.


## Hypotheses

### H0024: H0024: E0024-fb0024-make-hops-research-improvements-less-myopic の仮説


Source: `harness-lab/records/hypotheses/H0024-e0024-fb0024-make-hops-research-improvements-less-myopic.md`


# H0024: E0024-fb0024-make-hops-research-improvements-less-myopic の仮説

## 仮説

Add an explicit horizon/generalization gate to hops-research-improvements so agents group narrow observations, park local-only frictions, and promote at most one systemic candidate before creating lab records or issues.

## メカニズム

採用前に、提案変更が作用するメカニズムを明示してください。曖昧なプロセス追加や文書追加だけでは証拠として不十分です。

## 最小実装

紐づく評価ケースで評価できる最も狭い変更を実装してください。複雑さを減らせるなら、新しい抽象より削除または統合を優先します。

## 代替案: 削除または統合

新しい挙動を追加する前に、既存のルール、プロファイル、スキル、テンプレートを削除、統合、厳格化できないか評価してください。

## 期待される利点

紐づく評価ケース `E0024` が、運用者負担を減らし、プロジェクト固有文脈を上流へ漏らさずに通る。

## 想定される欠点

想定される欠点: ルーティング摩擦、偽陽性、保守負担が増える可能性。採用にはこの点の明示的な確認が必要です。

## 評価計画

`hops eval --case E0024 --manual` を実行し、採用判断を作る前に多軸スコアを記録する。

## 中止基準

紐づく評価ケースを改善しない、プライバシーリスクを増やす、または失敗クラスを減らさずにガバナンス構造だけを追加する場合、この仮説を却下または保留する。


## Evidence

`harness-lab/views/eval-results/E0024-manual-score.md`

## Guard

- status: implemented
- path: tests/test_agent_harness_contract.py

## Links

- issue_url: https://github.com/Nkzono99/harnessops/issues/11

## Open Questions And Next Action

次の実装または評価ステップは、この dossier と紐づく正規化レコードを更新してから再生成してください。

## Decision Log

### D0025: D0025: adopted H0024


Source: `harness-lab/records/decisions/D0025-adopted-h0024.md`


# D0025: adopted H0024

## 判断

adopted

## 理由

Issue #11 acceptance criteria are covered by a skill-level anti-myopia strategy pass and packaging contract tests.

## 証拠

Updated repo-local and packaged hops-research-improvements skills; uv run pytest tests/test_agent_harness_contract.py; uv run ruff check tests/test_agent_harness_contract.py; manual eval E0024.

## 回帰リスク

Low. The change is guidance text plus contract assertions; it narrows when new records are created and preserves urgent guardrail capture for broader failure classes.

## フォローアップ

Watch future research-scan runs for over-parking genuinely urgent guardrails.

## 回帰ガード

tests/test_agent_harness_contract.py
