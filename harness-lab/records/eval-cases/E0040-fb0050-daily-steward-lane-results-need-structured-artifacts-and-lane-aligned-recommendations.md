---
id: E0040
record_type: eval_case
created_at: '2026-05-18T03:19:15+09:00'
status: active
capability: daily_steward_supervision
failure_class: implicit_lane_contract
source_feedback: FB0050
---

# E0040: FB0050-daily-steward-lane-results-need-structured-artifacts-and-lane-aligned-recommendations を評価

## フィクスチャ

- source_feedback: `harness-lab/records/feedback/FB0050-daily-steward-lane-results-need-structured-artifacts-and-lane-aligned-recommendations.md`
- fixture_dir: `harness-lab/records/eval-cases/fixtures/E0040`
- observation: Code review found that open-meta-scan results were only described by handoff prose, while subagent spawn recommendations used signal names that did not always match supervisor lane names. This can make downstream invention/priority agents depend on implicit formatting or nonexistent lane identifiers.

## タスク

`daily_steward_supervision` の `implicit_lane_contract` を減らす最小変更を設計または実装し、次の再現条件が解消されるか評価してください。

Review merged PR #30 and inspect src/harnessops/core/steward.py plus daily steward preflight JSON.

## 期待される挙動

Steward run preflight should expose optional structured lane artifacts for open-meta-scan raw ideas/counterframes/routing hints, and subagent spawn recommendations should align with actual supervisor lanes while keeping signal detail available separately.

## 合格基準

- `implicit_lane_contract` の再現条件が検出または防止される。
- 提案または実装される変更が source feedback の期待変更に対応している。
- `hops lab eval --case E0040 --manual` の score と notes で採用判断に必要な証拠を説明できる。
- 非公開プロジェクト詳細を追加で要求しない。

## 不合格基準

- `implicit_lane_contract` の再現条件を見逃す。
- source feedback の期待変更と無関係な改善案になる。
- 評価が yml score へ記録されず、採用判断の証拠として追えない。
- 再現または判断に非公開文脈が必要になる。
