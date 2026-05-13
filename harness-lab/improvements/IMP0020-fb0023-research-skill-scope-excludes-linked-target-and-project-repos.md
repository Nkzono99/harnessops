---
id: IMP0020
record_type: improvement_dossier
created_at: '2026-05-13T17:59:46+09:00'
updated_at: '2026-05-13T18:05:27+09:00'
status: adopted
source_type: friction
scope: harnessops-core
maturity: adopted
relation: extends
promotion_level: target-lab-case
source_feedback: FB0023
eval_cases:
- E0023
hypotheses:
- H0023
decisions:
- D0024
research_scans: []
classification:
  capability: harness_lab_traceability
  failure_class: missing_lab_capture
guard:
  status: implemented
  path: tests/test_agent_harness_contract.py::test_meta_improvement_research_skill_is_packaged
investigation:
- created_at: '2026-05-13T18:00:01+09:00'
  kind: codebase
  summary: Repo-local skills are packaged for target/project repositories, but hops-research-improvements currently frames itself as HarnessOps meta improvement research and assumes harness-lab commands. Project repositories should instead record observed failures through harness-feedback and route/export sanitized feedback, while target or meta repositories can use harness-lab research-scan/eval/propose directly.
  evidence_ref: .agents/skills/hops-research-improvements/SKILL.md
links:
  issue_url:
---

# IMP0020: FB0023: Research skill scope excludes linked target and project repos

## Status

- status: adopted
- maturity: adopted
- source_type: friction
- scope: harnessops-core
- relation: extends
- promotion_level: target-lab-case
- source_feedback: `FB0023`
- linked_records: `FB0023`, `E0023`, `H0023`, `D0024`

## Source Observation

Source: `harness-lab/records/feedback/FB0023-research-skill-scope-excludes-linked-target-and-project-repos.md`

# FB0023: Research skill scope excludes linked target and project repos

## 概要

The hops-research-improvements skill description says it is for HarnessOps meta improvements, which makes it sound like a HarnessOps-core-only tool even though repo-local skills are also deployed into linked target and project repositories. Agents in those repositories should be able to use the same research workflow for target/project harness improvements while preserving the correct lab versus feedback routing.

## 再現

ローカル改善作業中に観測。

## 期待する上流変更

The skill and packaged copies should explicitly support HarnessOps core, target repositories with harness-lab, and project repositories with harness-feedback, with guidance for routing research outputs through the right HOPS commands.

## Target Capability

- capability: harness_lab_traceability
- failure_class: missing_lab_capture

## Investigation

- 2026-05-13T18:00:01+09:00 [codebase] Repo-local skills are packaged for target/project repositories, but hops-research-improvements currently frames itself as HarnessOps meta improvement research and assumes harness-lab commands. Project repositories should instead record observed failures through harness-feedback and route/export sanitized feedback, while target or meta repositories can use harness-lab research-scan/eval/propose directly. (evidence: .agents/skills/hops-research-improvements/SKILL.md)

## Research Scans

research scan はまだありません。


## Evaluation

### E0023: E0023: FB0023-research-skill-scope-excludes-linked-target-and-project-repos を評価


- source: `harness-lab/records/eval-cases/E0023-fb0023-research-skill-scope-excludes-linked-target-and-project-repos.md`

- capability: harness_lab_traceability

- failure_class: missing_lab_capture

- manual_eval_yml: `harness-lab/views/eval-results/E0023-manual-score.yml`
- manual_eval_md: `harness-lab/views/eval-results/E0023-manual-score.md`
- scores: impact=4, mechanism_clarity=5, evaluability=5, minimality=4, regression_risk=2, operator_burden=2, anti_theater=5, maintainability=4, privacy_sanitization_risk=2
- notes: Broadened hops-research-improvements to HarnessOps core plus linked target/project repositories. The skill now branches by repo role: target/meta lab repos use research-scan/investigate/classify/capture/propose, while project repos use failure/feedback/export and must not create harness-lab. Packaged Codex/Claude skill copies, docs, and contract tests were updated. Focused tests, full pytest, ruff, doctor, and migrate all passed.


## Hypotheses

### H0023: H0023: E0023-fb0023-research-skill-scope-excludes-linked-target-and-project-repos の仮説


Source: `harness-lab/records/hypotheses/H0023-e0023-fb0023-research-skill-scope-excludes-linked-target-and-project-repos.md`


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


## Evidence

`harness-lab/views/eval-results/E0023-manual-score.md`

## Guard

- status: implemented
- path: tests/test_agent_harness_contract.py::test_meta_improvement_research_skill_is_packaged

## Links

- issue_url: 未設定

## Open Questions And Next Action

次の実装または評価ステップは、この dossier と紐づく正規化レコードを更新してから再生成してください。

## Decision Log

### D0024: D0024: adopted H0023


Source: `harness-lab/records/decisions/D0024-adopted-h0023.md`


# D0024: adopted H0023

## 判断

adopted

## 理由

Adopted because repo-local research improvements should be usable wherever HarnessOps is installed, with role-aware routing to lab or feedback workflows.

## 証拠

tests/test_agent_harness_contract.py; pytest -q; ruff check .; hops doctor --check-overlay --check-records; hops migrate --check.

## 回帰リスク

Medium-low; this broadens instructions, but contract tests preserve packaged skill equality and explicitly guard the project-repo no-harness-lab rule.

## フォローアップ

変更を昇格する前にこの判断をレビューしてください。

## 回帰ガード

tests/test_agent_harness_contract.py::test_meta_improvement_research_skill_is_packaged
