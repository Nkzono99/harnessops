---
id: H0021
record_type: hypothesis
created_at: '2026-05-13T17:17:49+09:00'
status: proposed
target_capability: unclassified
source_eval_case: E0021
---

# H0021: E0021-fb0021-packaged-agent-skill-assets-still-document-editable-hops-fallback の仮説

## 仮説

Packaged agent assets should guide downstream agents to a PyPI-backed hops invocation when hops is not on PATH.

## メカニズム

Replace editable checkout fallback text in generated bridge, packaged Codex/Claude skill assets, and packaged plugin READMEs with uvx --from harnessops hops; keep editable commands only in HarnessOps repository development docs.

## 最小実装

Update BRIDGE_TEXT, packaged plugin skill/readme assets, source package asset copies, and contract tests that reject editable fallback in packaged assets.

## 代替案: 削除または統合

新しい挙動を追加する前に、既存のルール、プロファイル、スキル、テンプレートを削除、統合、厳格化できないか評価してください。

## 期待される利点

紐づく評価ケース `E0021` が、運用者負担を減らし、プロジェクト固有文脈を上流へ漏らさずに通る。

## 想定される欠点

想定される欠点: ルーティング摩擦、偽陽性、保守負担が増える可能性。採用にはこの点の明示的な確認が必要です。

## 評価計画

Run agent harness contract tests and grep packaged/generated assets to confirm uvx fallback is present and editable fallback is absent from target-facing assets.

## 中止基準

Reject if HarnessOps repository development workflows lose their editable checkout commands or generated target skills still mention uv run --with-editable . hops <command>.
