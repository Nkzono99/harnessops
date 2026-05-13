---
id: H0023
record_type: hypothesis
created_at: '2026-05-13T18:00:16+09:00'
status: proposed
target_capability: harness_lab_traceability
source_eval_case: E0023
---

# H0023: E0023-fb0023-research-skill-scope-excludes-linked-target-and-project-repos の仮説

## 仮説

Broadening hops-research-improvements to linked target and project repositories will make repo-local research workflows usable where HarnessOps is installed, without encouraging project repos to write harness-lab records directly.

## メカニズム

Update the skill description and body to classify the current repository from .harnessops/project.toml, branch commands by overlay type, and distinguish target/meta lab research from project feedback capture/export. Mirror the change into packaged Codex/Claude assets and contract tests.

## 最小実装

Edit the repo-local skill, plugin skill copies, package asset copies, docs, and tests so target/project applicability and routing commands are explicit.

## 代替案: 削除または統合

新しい挙動を追加する前に、既存のルール、プロファイル、スキル、テンプレートを削除、統合、厳格化できないか評価してください。

## 期待される利点

紐づく評価ケース `E0023` が、運用者負担を減らし、プロジェクト固有文脈を上流へ漏らさずに通る。

## 想定される欠点

想定される欠点: ルーティング摩擦、偽陽性、保守負担が増える可能性。採用にはこの点の明示的な確認が必要です。

## 評価計画

Run agent harness contract tests, focused MVP tests if update-harness refreshes managed skill copies, full pytest, ruff, doctor, and migrate.

## 中止基準

Reject if the skill tells project repositories to create harness-lab records directly, loses the research-scan flow for target/meta repositories, or causes packaged skills to diverge from repo-local skills.
