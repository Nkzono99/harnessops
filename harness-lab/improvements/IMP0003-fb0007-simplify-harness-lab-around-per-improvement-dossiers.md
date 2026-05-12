---
id: IMP0003
record_type: improvement_dossier
created_at: '2026-05-13T00:21:17+09:00'
updated_at: '2026-05-13T00:24:59+09:00'
status: adopted
source_feedback: FB0007
eval_cases:
- E0007
hypotheses:
- H0007
decisions:
- D0008
classification:
  capability: unclassified
  failure_class: unclassified
links:
  issue_url: https://github.com/Nkzono99/harnessops/issues/7
---

# IMP0003: FB0007: Simplify harness-lab around per-improvement dossiers

## Status

- status: adopted
- source_feedback: `FB0007`
- linked_records: `FB0007`, `E0007`, `H0007`, `D0008`

## Source Observation

Source: `harness-lab/records/feedback/FB0007-simplify-harness-lab-around-per-improvement-dossiers.md`

# FB0007: Simplify harness-lab around per-improvement dossiers

## 概要

GitHub issue: https://github.com/Nkzono99/harnessops/issues/7
author: Nkzono99
labels: enhancement
created_at: 2026-05-12T14:53:47Z
updated_at: 2026-05-12T14:53:47Z

## Issue本文
## Context

`harness-lab/` has a good theory: GitHub Issues remain the task tracker, while the lab keeps evaluation memory, hypotheses, experiments, and decisions.

In actual use, the current structure feels too heavy for the common case. A single improvement can quickly spread across multiple thin files and directories:

- `records/feedback/FB0001-...md`
- `records/eval-cases/E0001-...md`
- `records/hypotheses/H0001-...md`
- `records/experiments/`
- `records/decisions/D0001-...md`
- generated views under `views/`

The individual files are often mostly boilerplate at the moment they are created. More importantly, the workflow for recording an improvement and later using that record during implementation/review is not yet obvious enough.

## Concern

For day-to-day harness improvement, this may create more bookkeeping than memory:

- The directory structure is cognitively expensive.
- The relationship between feedback, eval case, hypothesis, experiment, and decision is hard to scan.
- The content starts thin, so agents/users may create records but not return to them.
- The capture path exists, but the “use this while improving the harness” path is underdeveloped.
- It is unclear which file is the living source of truth for one improvement.

## Proposal

Consider making the ordinary workflow centered on one mutable improvement dossier per improvement, for example:

```text
harness-lab/improvements/IMP0001-promote-improve-harness-workflow.md
```

A dossier could contain sections such as:

- status and current decision
- source observation / feedback
- target capability or failure class
- hypothesis and mechanism
- eval plan and acceptance criteria
- experiments and evidence
- links to GitHub issues / PRs / commits
- open questions and next action
- decision log / changelog

Generated views can then be derived from these dossiers: backlog, active improvements, decisions, score trajectory, and open eval gaps.

The current typed records (`FB`, `E`, `H`, `X`, `D`) could remain as an advanced or normalized layer, but should not be mandatory for the common “record and improve one thing” flow.

## Acceptance criteria

- There is a low-friction command to create or update one improvement dossier.
- A user or agent can open one file and understand the full improvement history.
- Generated views still support triage and review.
- Existing `harness-lab/records/*` layouts have a migration or compatibility story.
- The docs explain when to use a simple dossier versus the normalized multi-record flow.

## 再現

送信元フィードバックバンドルを参照してください。

## 期待する上流変更

送信元フィードバックバンドルを参照してください。

## Target Capability

- capability: unclassified
- failure_class: unclassified

## Evaluation

### E0007: E0007: FB0007-simplify-harness-lab-around-per-improvement-dossiers を評価


Source: `harness-lab/records/eval-cases/E0007-fb0007-simplify-harness-lab-around-per-improvement-dossiers.md`


# E0007: FB0007-simplify-harness-lab-around-per-improvement-dossiers を評価

## フィクスチャ

フィクスチャディレクトリ: `harness-lab/records/eval-cases/fixtures/E0007`。

## タスク

この失敗を防ぐべき挙動を記述してください。

## 期待される挙動

ターゲットハーネスが、非公開プロジェクト文脈を漏らさずに失敗クラスを扱います。

## 合格基準

- 失敗条件が検出または防止される。
- 提案される挙動が上流メンテナにとって実行可能である。
- 非公開プロジェクト詳細を必要としない。

## 不合格基準

- 失敗を見逃す。
- 再現に非公開文脈が必要になる。


## Hypotheses

### H0007: H0007: E0007-fb0007-simplify-harness-lab-around-per-improvement-dossiers の仮説


Source: `harness-lab/records/hypotheses/H0007-e0007-fb0007-simplify-harness-lab-around-per-improvement-dossiers.md`


# H0007: E0007-fb0007-simplify-harness-lab-around-per-improvement-dossiers の仮説

## 仮説

普通の harness 改善を one improvement dossier に集約し、typed records は派生または advanced layer にすると、日常運用の記録コストを下げながら評価記憶を保てる。

## メカニズム

harness-lab/improvements/IMPxxxx を living source of truth にし、status、source observation、hypothesis、eval plan、evidence、links、decision log を同一ファイルに置き、views はそこから生成する。

## 最小実装

新規 dossier 作成/更新コマンドを追加し、既存 records/* は互換読み取りまたは migration path として残す。

## 代替案: 削除または統合

現在の FB/E/H/X/D 正規化レイアウトを維持し、views と docs だけで見通しを改善する。

## 期待される利点

agent とユーザーが一つのファイルを開けば改善履歴を追えるようになり、lab が戻ってくる場所として機能しやすくなる。

## 想定される欠点

既存の正規化レコード、score trajectory、decision workflow との対応関係が曖昧になる可能性がある。

## 評価計画

既存 issue #5〜#8 を dossier 形式で表現できるか試し、backlog/imported-feedback/score views と migration docs が破綻しないことを確認する。

## 中止基準

dossier が自由記述ノートになり、評価ケースや採用判断の証拠を機械的に追えなくなる場合は採用しない。


## Evidence

`harness-lab/views/eval-results/E0007-manual-score.md`

## Links

- issue_url: https://github.com/Nkzono99/harnessops/issues/7

## Open Questions And Next Action

次の実装または評価ステップは、この dossier と紐づく正規化レコードを更新してから再生成してください。

## Decision Log

### D0008: D0008: adopted H0007


Source: `harness-lab/records/decisions/D0008-adopted-h0007.md`


# D0008: adopted H0007

## 判断

adopted

## 理由

H0007 の最小実装を採用。正規化レコードは正本として残し、日常レビュー用に IMP dossier を生成/更新する互換レイヤーを追加した。

## 証拠

Tests: uv run pytest tests/test_cli/test_mvp_flow.py tests/test_agent_harness_contract.py; uv run pytest; uv run ruff check src/harnessops/core/records.py src/harnessops/cli/lab.py src/harnessops/core/render.py src/harnessops/core/overlay.py tests/test_cli/test_mvp_flow.py; hops doctor --check-overlay --check-records; hops migrate --check. Generated dossiers: IMP0001-IMP0004. Manual eval: harness-lab/views/eval-results/E0007-manual-score.yml

## 回帰リスク

Moderate-low. Dossiers are generated from existing records and do not replace the normalized source of truth; new managed view introduction required refresh_views to register generated view hashes.

## フォローアップ

Consider adding richer dossier update options after the lab-first issue workflow is implemented.

## 回帰ガード

tests/test_cli/test_mvp_flow.py

