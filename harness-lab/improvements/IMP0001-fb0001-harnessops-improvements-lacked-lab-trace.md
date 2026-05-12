---
id: IMP0001
record_type: improvement_dossier
created_at: '2026-05-13T00:20:57+09:00'
updated_at: '2026-05-13T00:23:11+09:00'
status: adopted
source_feedback: FB0001
eval_cases:
- E0001
hypotheses:
- H0001
decisions:
- D0001
classification:
  capability: harness_lab_traceability
  failure_class: missing_lab_capture
links:
  issue_url:
---

# IMP0001: FB0001: HarnessOps improvements lacked lab trace

## Status

- status: adopted
- source_feedback: `FB0001`
- linked_records: `FB0001`, `E0001`, `H0001`, `D0001`

## Source Observation

Source: `harness-lab/records/feedback/FB0001-harnessops-improvements-lacked-lab-trace.md`

# FB0001: HarnessOps improvements lacked lab trace

## 概要

HarnessOps CLI and skill improvements could be implemented, committed, released, and published without any harness-lab record.

## 再現

Run a nontrivial HarnessOps improvement from local conversation without an upstream feedback bundle or GitHub issue. Existing hops-run-lab guidance assumed an FB record already existed.

## 期待する上流変更

Provide a first-class lab capture command and update agent, release, and lab skills so local HarnessOps improvements start with a harness-lab record.

## Target Capability

- capability: harness_lab_traceability
- failure_class: missing_lab_capture

## Evaluation

### E0001: E0001: FB0001-harnessops-improvements-lacked-lab-trace を評価


Source: `harness-lab/records/eval-cases/E0001-fb0001-harnessops-improvements-lacked-lab-trace.md`


# E0001: FB0001-harnessops-improvements-lacked-lab-trace を評価

## フィクスチャ

フィクスチャディレクトリ: `harness-lab/records/eval-cases/fixtures/E0001`。

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

### H0001: H0001: E0001-fb0001-harnessops-improvements-lacked-lab-trace の仮説


Source: `harness-lab/records/hypotheses/H0001-e0001-fb0001-harnessops-improvements-lacked-lab-trace.md`


# H0001: E0001-fb0001-harnessops-improvements-lacked-lab-trace の仮説

## 仮説

A first-class lab capture command plus agent and release guidance will make local HarnessOps improvements traceable before release.

## メカニズム

The command creates an FB record directly from local observations without requiring an external issue or sanitized bundle, and the skills/docs remind agents to use it.

## 最小実装

Add hops lab capture, tests, documentation, repo-local skill guidance, and release-skill checks.

## 代替案: 削除または統合

Require a GitHub issue or manual record creation before every HarnessOps improvement.

## 期待される利点

Nontrivial HarnessOps changes have an explicit feedback, eval, hypothesis, and decision trail.

## 想定される欠点

Small changes may feel like they carry extra record-keeping overhead.

## 評価計画

Exercise lab capture in CLI tests, assert skill/docs mention it, run full pytest and doctor with record validation.

## 中止基準

If agents still bypass lab records or the command creates low-value noise, simplify the trigger rule or add a stronger release gate.


## Evidence

`harness-lab/views/eval-results/E0001-manual-score.md`

## Links

- issue_url: 未設定

## Open Questions And Next Action

次の実装または評価ステップは、この dossier と紐づく正規化レコードを更新してから再生成してください。

## Decision Log

### D0001: D0001: adopted H0001


Source: `harness-lab/records/decisions/D0001-adopted-h0001.md`


# D0001: adopted H0001

## 判断

adopted

## 理由

The missing trace was caused by a weak first-step workflow, not by absent storage. A dedicated capture command plus skill and release guidance closes that gap with minimal new surface.

## 証拠

See harness-lab/views/eval-results/E0001-manual-score.yml and tests/test_cli/test_mvp_flow.py::test_lab_capture_records_local_improvement.

## 回帰リスク

Low. The new command only writes harness-lab records in upstream-lab/meta-lab modes and reuses existing record validation.

## フォローアップ

変更を昇格する前にこの判断をレビューしてください。

## 回帰ガード

tests/test_cli/test_mvp_flow.py

