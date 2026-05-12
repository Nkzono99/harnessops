---
id: IMP0011
record_type: improvement_dossier
created_at: '2026-05-13T02:04:58+09:00'
updated_at: '2026-05-13T02:27:15+09:00'
status: adopted
source_type: failure
scope: harnessops-core
maturity: adopted
relation: new
promotion_level: target-lab-case
source_feedback: FB0014
eval_cases:
- E0013
hypotheses:
- H0013
decisions:
- D0014
classification:
  capability: lab_record_consistency
  failure_class: duplicate_improvement_dossier_race
guard:
  status: implemented
  path: tests/test_cli/test_mvp_flow.py
investigation:
- created_at: '2026-05-13T02:05:22+09:00'
  kind: codebase
  summary: create_or_update_improvement_dossier first scans existing IMP files by source_feedback and otherwise allocates next_id from the directory. Without locking or duplicate validation, concurrent commands can both miss the existing dossier and allocate different IMP IDs. Current doctor validates individual records but not uniqueness of source_feedback across improvement dossiers.
  evidence_ref: src/harnessops/core/records.py::_find_existing_dossier ; src/harnessops/core/records.py::create_or_update_improvement_dossier ; src/harnessops/core/validation.py::doctor
- created_at: '2026-05-13T02:20:55+09:00'
  kind: implementation
  summary: While implementing the duplicate dossier fix, generated records and eval/issue draft outputs again triggered Windows CRLF diff-check noise. The patch now writes HarnessOps generated records, manual eval results, and issue drafts with newline='\n' so generated lab artifacts stay stable on Windows.
  evidence_ref: src/harnessops/core/records.py ; src/harnessops/core/evaluation.py ; src/harnessops/cli/lab.py ; src/harnessops/cli/feedback.py
links:
  issue_url:
---

# IMP0011: FB0014: Prevent duplicate improvement dossiers from concurrent lab commands

## Status

- status: adopted
- maturity: adopted
- source_type: failure
- scope: harnessops-core
- relation: new
- promotion_level: target-lab-case
- source_feedback: `FB0014`
- linked_records: `FB0014`, `E0013`, `H0013`, `D0014`

## Source Observation

Source: `harness-lab/records/feedback/FB0014-prevent-duplicate-improvement-dossiers-from-concurrent-lab-commands.md`

# FB0014: Prevent duplicate improvement dossiers from concurrent lab commands

## 概要

Running lab dossier, lab classify, and lab investigate concurrently for the same source feedback created two improvement dossiers for FB0013. Doctor did not detect the duplicate source_feedback mapping.

## 再現

Invoke multiple hops lab commands for a new FB in parallel, such as dossier/classify/investigate. Each command can call create_or_update_improvement_dossier before another command's new dossier is visible, causing duplicate IMP records.

## 期待する上流変更

Make improvement dossier creation idempotent under concurrent calls or add doctor validation that detects duplicate IMP source_feedback values and tells the operator how to repair them.

## Target Capability

- capability: lab_record_consistency
- failure_class: duplicate_improvement_dossier_race

## Investigation

- 2026-05-13T02:05:22+09:00 [codebase] create_or_update_improvement_dossier first scans existing IMP files by source_feedback and otherwise allocates next_id from the directory. Without locking or duplicate validation, concurrent commands can both miss the existing dossier and allocate different IMP IDs. Current doctor validates individual records but not uniqueness of source_feedback across improvement dossiers. (evidence: src/harnessops/core/records.py::_find_existing_dossier ; src/harnessops/core/records.py::create_or_update_improvement_dossier ; src/harnessops/core/validation.py::doctor)
- 2026-05-13T02:20:55+09:00 [implementation] While implementing the duplicate dossier fix, generated records and eval/issue draft outputs again triggered Windows CRLF diff-check noise. The patch now writes HarnessOps generated records, manual eval results, and issue drafts with newline='\n' so generated lab artifacts stay stable on Windows. (evidence: src/harnessops/core/records.py ; src/harnessops/core/evaluation.py ; src/harnessops/cli/lab.py ; src/harnessops/cli/feedback.py)

## Evaluation

### E0013: E0013: FB0014-prevent-duplicate-improvement-dossiers-from-concurrent-lab-commands を評価


Source: `harness-lab/records/eval-cases/E0013-fb0014-prevent-duplicate-improvement-dossiers-from-concurrent-lab-commands.md`


# E0013: FB0014-prevent-duplicate-improvement-dossiers-from-concurrent-lab-commands を評価

## フィクスチャ

フィクスチャディレクトリ: `harness-lab/records/eval-cases/fixtures/E0013`。

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

### H0013: H0013: E0013-fb0014-prevent-duplicate-improvement-dossiers-from-concurrent-lab-commands の仮説


Source: `harness-lab/records/hypotheses/H0013-e0013-fb0014-prevent-duplicate-improvement-dossiers-from-concurrent-lab-commands.md`


# H0013: E0013-fb0014-prevent-duplicate-improvement-dossiers-from-concurrent-lab-commands の仮説

## 仮説

Improvement dossier creation should be source-feedback-idempotent and doctor should detect duplicate source_feedback mappings, so concurrent lab commands cannot silently leave two dossiers for one feedback record.

## メカニズム

A short per-source lock around create_or_update_improvement_dossier serializes dossier creation, while doctor validates improvements/IMP*.md and reports duplicate source_feedback values as record consistency errors.

## 最小実装

Add a file-based source_feedback lock for dossier creation, include improvement dossiers in doctor record validation, add duplicate source_feedback validation, and cover evidence_ref rendering in dossier investigation output.

## 代替案: 削除または統合

Only document that lab commands must be run serially, but Codex and other agents naturally parallelize tool calls, so documentation would not prevent the failure.

## 期待される利点

Lab state remains one dossier per feedback source, doctor catches preexisting duplicates, and investigation evidence is visible during review.

## 想定される欠点

The lock adds small runtime complexity and must avoid stale-lock deadlocks.

## 評価計画

Add tests that doctor rejects duplicate improvement dossiers and that repeated/parallel dossier creation returns one file; verify dossier investigation renders evidence refs; run focused CLI/core tests and full test suite.

## 中止基準

If the lock can deadlock normal lab commands or duplicate detection creates false positives for valid dossier relations, replace it with deterministic repair guidance only.


## Evidence

`harness-lab/views/eval-results/E0013-manual-score.md`

## Guard

- status: implemented
- path: tests/test_cli/test_mvp_flow.py

## Links

- issue_url: 未設定

## Open Questions And Next Action

次の実装または評価ステップは、この dossier と紐づく正規化レコードを更新してから再生成してください。

## Decision Log

### D0014: D0014: adopted H0013


Source: `harness-lab/records/decisions/D0014-adopted-h0013.md`


# D0014: adopted H0013

## 判断

adopted

## 理由

The dry-run exposed an actual consistency failure from concurrent lab commands, and the implemented lock plus doctor validation prevents silent duplicate dossiers while preserving the existing dossier workflow.

## 証拠

tests/test_cli/test_mvp_flow.py covers parallel dossier creation, duplicate source_feedback doctor failure, and evidence_ref rendering; uv run pytest tests/test_cli/test_mvp_flow.py -q; hops doctor --check-overlay --check-records

## 回帰リスク

Medium-low: the file lock adds runtime behavior, but it is scoped to source_feedback, has a timeout, and stale lock cleanup.

## フォローアップ

変更を昇格する前にこの判断をレビューしてください。

## 回帰ガード

tests/test_cli/test_mvp_flow.py
