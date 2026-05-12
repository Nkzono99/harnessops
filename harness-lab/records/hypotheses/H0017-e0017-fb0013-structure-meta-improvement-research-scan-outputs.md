---
id: H0017
record_type: hypothesis
created_at: '2026-05-13T03:25:39+09:00'
status: proposed
target_capability: meta_improvement_research
source_eval_case: E0017
---

# H0017: E0017-fb0013-structure-meta-improvement-research-scan-outputs の仮説

## 仮説

A hops lab research-scan record can turn meta-improvement research output into a structured, source-linked artifact before agents decide whether to investigate, capture, propose, park, or reject candidates.

## メカニズム

The command stores scope, evidence groups, candidate rows, relations, recommendations, and next commands in a canonical RS record plus a generated summary view, so research results stop living only in chat prose or free-form investigation notes.

## 最小実装

Add a research_scan record type, a hops lab research-scan CLI command, generated view support, validation, docs, packaged skill guidance, and tests that assert structured candidates and evidence are recorded.

## 代替案: 削除または統合

Keep using free-form hops lab investigate summaries only, but that loses candidate boundaries and makes later routing or compaction harder.

## 期待される利点

Meta-improvement research can be reviewed, routed, compacted, and converted into lab actions without rereading chat history.

## 想定される欠点

Another record type can add surface area, so keep it lightweight and only use it for deliberate research scans rather than every small observation.

## 評価計画

Create a research scan in a fixture repo, assert RS frontmatter/body/view capture evidence and candidates, then run contract tests for packaged skills and full validation.

## 中止基準

Reject if the command bypasses existing lab flow, cannot link back to evidence, or encourages speculative candidate spam without recommendations or next commands.
