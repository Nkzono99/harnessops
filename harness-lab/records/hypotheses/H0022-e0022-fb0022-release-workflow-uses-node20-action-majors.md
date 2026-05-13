---
id: H0022
record_type: hypothesis
created_at: '2026-05-13T17:55:30+09:00'
status: proposed
target_capability: harness_lab_traceability
source_eval_case: E0022
---

# H0022: E0022-fb0022-release-workflow-uses-node20-action-majors の仮説

## 仮説

Updating the PyPI publish workflow to Node24-ready GitHub action majors will remove release-time Node20 deprecation risk without changing the build or publish semantics.

## メカニズム

Use actions/checkout@v5 and actions/setup-python@v6 in .github/workflows/publish-pypi.yml while keeping the existing Python 3.11, build, twine check, and trusted publisher steps unchanged.

## 最小実装

Edit the publish workflow action majors and add a repository test that asserts checkout@v5 and setup-python@v6 are used for the PyPI publish workflow.

## 代替案: 削除または統合

新しい挙動を追加する前に、既存のルール、プロファイル、スキル、テンプレートを削除、統合、厳格化できないか評価してください。

## 期待される利点

紐づく評価ケース `E0022` が、運用者負担を減らし、プロジェクト固有文脈を上流へ漏らさずに通る。

## 想定される欠点

想定される欠点: ルーティング摩擦、偽陽性、保守負担が増える可能性。採用にはこの点の明示的な確認が必要です。

## 評価計画

Run the workflow contract test, full pytest, ruff, hops doctor, and hops migrate; release-time validation can later confirm that GitHub no longer emits Node20 action annotations.

## 中止基準

Reject if the workflow stops publishing via the existing pypi environment, drops id-token permission, changes Python version unintentionally, or cannot be represented by a simple contract test.
