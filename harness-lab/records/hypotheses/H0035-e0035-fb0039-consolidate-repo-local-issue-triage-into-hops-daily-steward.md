---
id: H0035
record_type: hypothesis
created_at: '2026-05-14T11:10:24+09:00'
status: proposed
target_capability: unclassified
source_eval_case: E0035
---

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
