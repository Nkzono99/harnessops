---
id: IMP0008
record_type: improvement_dossier
created_at: '2026-05-13T01:43:17+09:00'
updated_at: '2026-05-13T02:22:13+09:00'
status: adopted
source_type: extension
scope: harnessops-core
maturity: adopted
relation: extends
promotion_level: harnessops-protocol
source_feedback: FB0012
eval_cases:
- E0012
hypotheses:
- H0012
decisions:
- D0013
classification:
  capability: meta_improvement_research
  failure_class: missing_research_skill
guard:
  status: implemented
  path: tests/test_agent_harness_contract.py
investigation:
- created_at: '2026-05-13T01:43:56+09:00'
  kind: external-benchmark
  summary: 'Manual meta-improvement research should borrow from external practice patterns: Google SRE stresses reviewed postmortem action items and repositories of learning; Open Practice Library experiment guidance stresses explicit hypotheses, measures, pass criteria, and learning; Technology Radar style maturity rings provide a useful model for non-binary promotion status.'
  evidence_ref: https://sre.google/sre-book/postmortem-culture/ ; https://openpracticelibrary.com/practice/design-of-experiments/ ; https://www.thoughtworks.com/radar/faq
- created_at: '2026-05-13T02:02:49+09:00'
  kind: dry-run
  summary: 'Dry-running hops-research-improvements exposed two extension gaps: the skill asks for candidate lists, evidence, and recommendations, but HarnessOps has no structured research-scan artifact or view; additionally, dossier bodies render investigation summaries but omit evidence_ref links, so external sources are less visible during review.'
  evidence_ref: src/harnessops/core/records.py::_format_investigation ; .agents/skills/hops-research-improvements/SKILL.md ; https://sre.google/sre-book/postmortem-culture/ ; https://openpracticelibrary.com/practice/design-of-experiments/ ; https://www.thoughtworks.com/radar/faq
links:
  issue_url:
---

# IMP0008: FB0012: Add manual meta improvement research skill

## Status

- status: adopted
- maturity: adopted
- source_type: extension
- scope: harnessops-core
- relation: extends
- promotion_level: harnessops-protocol
- source_feedback: `FB0012`
- linked_records: `FB0012`, `E0012`, `H0012`, `D0013`

## Source Observation

Source: `harness-lab/records/feedback/FB0012-add-manual-meta-improvement-research-skill.md`

# FB0012: Add manual meta improvement research skill

## 概要

HarnessOps needs a deliberate research skill for meta-level improvement discovery, separate from in-task meta-hypothesis scan. The skill should guide agents through codebase investigation, external web research, comparison, classification, and conversion into lab notes or hypotheses.

## 再現

The user asked for a skill that can be manually triggered to investigate meta-level improvement ideas, including codebase and web research, while still allowing future non-periodic autonomous triggering.

## 期待する上流変更

Add a packaged and repo-local HOPS skill for meta improvement research, with workflow steps, web/source requirements, output thresholds, and lab integration commands.

## Target Capability

- capability: meta_improvement_research
- failure_class: missing_research_skill

## Investigation

- 2026-05-13T01:43:56+09:00 [external-benchmark] Manual meta-improvement research should borrow from external practice patterns: Google SRE stresses reviewed postmortem action items and repositories of learning; Open Practice Library experiment guidance stresses explicit hypotheses, measures, pass criteria, and learning; Technology Radar style maturity rings provide a useful model for non-binary promotion status. (evidence: https://sre.google/sre-book/postmortem-culture/ ; https://openpracticelibrary.com/practice/design-of-experiments/ ; https://www.thoughtworks.com/radar/faq)
- 2026-05-13T02:02:49+09:00 [dry-run] Dry-running hops-research-improvements exposed two extension gaps: the skill asks for candidate lists, evidence, and recommendations, but HarnessOps has no structured research-scan artifact or view; additionally, dossier bodies render investigation summaries but omit evidence_ref links, so external sources are less visible during review. (evidence: src/harnessops/core/records.py::_format_investigation ; .agents/skills/hops-research-improvements/SKILL.md ; https://sre.google/sre-book/postmortem-culture/ ; https://openpracticelibrary.com/practice/design-of-experiments/ ; https://www.thoughtworks.com/radar/faq)

## Evaluation

### E0012: E0012: FB0012-add-manual-meta-improvement-research-skill を評価


Source: `harness-lab/records/eval-cases/E0012-fb0012-add-manual-meta-improvement-research-skill.md`


# E0012: FB0012-add-manual-meta-improvement-research-skill を評価

## フィクスチャ

フィクスチャディレクトリ: `harness-lab/records/eval-cases/fixtures/E0012`。

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

### H0012: H0012: E0012-fb0012-add-manual-meta-improvement-research-skill の仮説


Source: `harness-lab/records/hypotheses/H0012-e0012-fb0012-add-manual-meta-improvement-research-skill.md`


# H0012: E0012-fb0012-add-manual-meta-improvement-research-skill の仮説

## 仮説

A dedicated hops-research-improvements skill will make meta-level improvement discovery deliberate and evidence-backed without overloading the short in-task meta scan.

## メカニズム

The skill separates research mode from execution mode, requiring codebase review, existing dossier checks, external primary-source comparison when useful, candidate classification, and explicit lab commands for note/capture/propose outcomes.

## 最小実装

Add repo-local and packaged hops-research-improvements skills, document when to use the manual research lane, and guard packaging through contract tests.

## 代替案: 削除または統合

Fold the behavior into hops-run-lab only, but that makes ordinary lab work heavier and blurs short meta scans with deliberate research.

## 期待される利点

Agents can intentionally search for second-order improvements, compare against external practices, and turn only high-signal findings into HarnessOps lab records.

## 想定される欠点

Another skill can add surface area if its trigger is too broad or if it encourages speculative idea spam.

## 評価計画

Verify the skill is repo-local, packaged for Codex and Claude, mirrored into agent assets, references codebase and web research, and routes outputs through hops lab investigate/classify/capture/propose.

## 中止基準

If the skill cannot be distinguished from hops-run-lab or lacks tests that keep it packaged and lab-routed, reject or merge it back into hops-run-lab.


## Evidence

`harness-lab/views/eval-results/E0012-manual-score.md`

## Guard

- status: implemented
- path: tests/test_agent_harness_contract.py

## Links

- issue_url: 未設定

## Open Questions And Next Action

次の実装または評価ステップは、この dossier と紐づく正規化レコードを更新してから再生成してください。

## Decision Log

### D0013: D0013: adopted H0012


Source: `harness-lab/records/decisions/D0013-adopted-h0012.md`


# D0013: adopted H0012

## 判断

adopted

## 理由

A dedicated research skill cleanly separates deliberate meta-improvement investigation from the short work-in-progress meta scan, while routing all durable findings through lab dossier commands.

## 証拠

tests/test_agent_harness_contract.py packaging assertions; docs/design-principles.md manual meta improvement research section; harness-lab/views/eval-results/E0012-manual-score.md

## 回帰リスク

Medium: skill proliferation and speculative idea spam if triggers are vague.

## フォローアップ

変更を昇格する前にこの判断をレビューしてください。

## 回帰ガード

tests/test_agent_harness_contract.py
