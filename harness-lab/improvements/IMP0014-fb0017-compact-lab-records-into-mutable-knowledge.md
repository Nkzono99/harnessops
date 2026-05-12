---
id: IMP0014
record_type: improvement_dossier
created_at: '2026-05-13T02:53:30+09:00'
updated_at: '2026-05-13T03:10:56+09:00'
status: adopted
source_type: external-benchmark
scope: harnessops-core
maturity: adopted
relation: extends
promotion_level: harnessops-protocol
source_feedback: FB0017
eval_cases:
- E0016
hypotheses:
- H0016
decisions:
- D0017
classification:
  capability: lab_memory_compaction
  failure_class: record_sprawl_without_knowledge_consolidation
guard:
  status: implemented
  path: tests/test_cli/test_mvp_flow.py
investigation:
- created_at: '2026-05-13T02:53:41+09:00'
  kind: external-benchmark
  summary: Anthropic Managed Agents 'dreaming' is a scheduled process that reviews prior sessions and memory stores, extracts patterns, and curates memory; this supports a background/threshold compaction layer rather than stuffing all lab history into context.
  evidence_ref: https://claude.com/blog/new-in-claude-managed-agents
- created_at: '2026-05-13T02:53:53+09:00'
  kind: external-benchmark
  summary: Claude memory docs frame durable memory as client-controlled files that are created, read, updated, and deleted across sessions; HarnessOps should mirror that with local mutable knowledge files under harness-lab rather than append-only summaries only.
  evidence_ref: https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool
- created_at: '2026-05-13T02:54:05+09:00'
  kind: external-benchmark
  summary: Generative Agents and Reflexion both separate episodic traces from higher-level reflections; the lab should preserve records as episodic traces and compile recurring patterns, decisions, and guards into a smaller semantic layer.
  evidence_ref: https://arxiv.org/abs/2304.03442; https://arxiv.org/abs/2303.11366
- created_at: '2026-05-13T02:54:16+09:00'
  kind: external-benchmark
  summary: MemGPT and recent agent-memory surveys emphasize hierarchical context, write-manage-read loops, contradiction handling, privacy, and learned forgetting; HarnessOps compaction should be deterministic, source-linked, local, and reviewable.
  evidence_ref: https://arxiv.org/abs/2310.08560; https://arxiv.org/abs/2603.07670
links:
  issue_url: https://claude.com/blog/new-in-claude-managed-agents
---

# IMP0014: FB0017: Compact lab records into mutable knowledge

## Status

- status: adopted
- maturity: adopted
- source_type: external-benchmark
- scope: harnessops-core
- relation: extends
- promotion_level: harnessops-protocol
- source_feedback: `FB0017`
- linked_records: `FB0017`, `E0016`, `H0016`, `D0017`

## Source Observation

Source: `harness-lab/records/feedback/FB0017-compact-lab-records-into-mutable-knowledge.md`

# FB0017: Compact lab records into mutable knowledge

## 概要

As harness-lab grows, append-only records and generated dossiers will become too large to scan. The lab needs a compaction path that preserves canonical records while updating a smaller knowledge layer for reusable lessons, contradictions, guards, and promotion patterns.

## 再現

Accumulate feedback, eval cases, hypotheses, decisions, manual scores, and dossiers until reviewing harness-lab requires reading many files instead of consulting a compiled knowledge surface.

## 期待する上流変更

Provide a first-class lab compaction command that checks size thresholds, compiles source-linked mutable knowledge files, and leaves canonical records intact for audit and regeneration.

## Target Capability

- capability: lab_memory_compaction
- failure_class: record_sprawl_without_knowledge_consolidation

## Investigation

- 2026-05-13T02:53:41+09:00 [external-benchmark] Anthropic Managed Agents 'dreaming' is a scheduled process that reviews prior sessions and memory stores, extracts patterns, and curates memory; this supports a background/threshold compaction layer rather than stuffing all lab history into context. (evidence: https://claude.com/blog/new-in-claude-managed-agents)
- 2026-05-13T02:53:53+09:00 [external-benchmark] Claude memory docs frame durable memory as client-controlled files that are created, read, updated, and deleted across sessions; HarnessOps should mirror that with local mutable knowledge files under harness-lab rather than append-only summaries only. (evidence: https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool)
- 2026-05-13T02:54:05+09:00 [external-benchmark] Generative Agents and Reflexion both separate episodic traces from higher-level reflections; the lab should preserve records as episodic traces and compile recurring patterns, decisions, and guards into a smaller semantic layer. (evidence: https://arxiv.org/abs/2304.03442; https://arxiv.org/abs/2303.11366)
- 2026-05-13T02:54:16+09:00 [external-benchmark] MemGPT and recent agent-memory surveys emphasize hierarchical context, write-manage-read loops, contradiction handling, privacy, and learned forgetting; HarnessOps compaction should be deterministic, source-linked, local, and reviewable. (evidence: https://arxiv.org/abs/2310.08560; https://arxiv.org/abs/2603.07670)

## Evaluation

### E0016: E0016: FB0017-compact-lab-records-into-mutable-knowledge を評価


- source: `harness-lab/records/eval-cases/E0016-fb0017-compact-lab-records-into-mutable-knowledge.md`

- capability: lab_memory_compaction

- failure_class: record_sprawl_without_knowledge_consolidation

- manual_eval_yml: `harness-lab/views/eval-results/E0016-manual-score.yml`
- manual_eval_md: `harness-lab/views/eval-results/E0016-manual-score.md`
- scores: impact=4, mechanism_clarity=5, evaluability=5, minimality=4, regression_risk=3, operator_burden=4, anti_theater=4, maintainability=4, privacy_sanitization_risk=5
- notes: Compaction is deterministic, source-linked, and guarded by CLI tests. It preserves canonical records and keeps manual Curator Notes mutable, so it reduces review load without turning summaries into adoption evidence.


## Hypotheses

### H0016: H0016: E0016-fb0017-compact-lab-records-into-mutable-knowledge の仮説


Source: `harness-lab/records/hypotheses/H0016-e0016-fb0017-compact-lab-records-into-mutable-knowledge.md`


# H0016: E0016-fb0017-compact-lab-records-into-mutable-knowledge の仮説

## 仮説

A hops lab compact command can keep long-running lab work usable by compiling canonical records into source-linked mutable knowledge files.

## メカニズム

The command measures lab size, exits without writing until thresholds are exceeded unless forced, then updates a compact knowledge map from feedback, dossier, decision, score, guard, and investigation metadata. Canonical records remain the audit log; knowledge files become the mutable working memory.

## 最小実装

Add a deterministic compaction core, a hops lab compact CLI with threshold and force options, docs/spec coverage, and tests that verify threshold gating, source links, scores, guards, and doctor compatibility.

## 代替案: 削除または統合

Do not archive or delete records first. Avoid adding another append-only record family; use a regenerated mutable knowledge layer with source hashes and timestamps.

## 期待される利点

Agents and humans can consult a compact lab memory once harness-lab grows, while still being able to trace every knowledge item back to records and dossiers.

## 想定される欠点

A stale or overconfident summary could hide important contradictions, so the output must preserve source IDs, threshold metadata, and warnings rather than replacing records.

## 評価計画

Run focused CLI tests for forced compaction and threshold skip behavior, then full pytest, ruff, doctor, and migrate checks.

## 中止基準

Reject or park if the command mutates canonical records, drops source traceability, requires network or model calls, or makes doctor fail on generated knowledge files.


## Evidence

`harness-lab/views/eval-results/E0016-manual-score.md`

## Guard

- status: implemented
- path: tests/test_cli/test_mvp_flow.py

## Links

- issue_url: https://claude.com/blog/new-in-claude-managed-agents

## Open Questions And Next Action

次の実装または評価ステップは、この dossier と紐づく正規化レコードを更新してから再生成してください。

## Decision Log

### D0017: D0017: adopted H0016


Source: `harness-lab/records/decisions/D0017-adopted-h0016.md`


# D0017: adopted H0016

## 判断

adopted

## 理由

The implementation gives harness-lab a threshold-gated compaction path that preserves records and creates a mutable, source-linked knowledge layer for long-running labs.

## 証拠

Focused tests cover forced compaction, threshold skipping, source-linked capability knowledge, score summaries, guard index, Curator Notes preservation, and doctor compatibility.

## 回帰リスク

Moderate: summaries can become stale or over-trusted, mitigated by source IDs, source digest, no record deletion, and tests that preserve the source-linked contract.

## フォローアップ

Use hops lab compact --force after large lab updates or release-prep reviews; later work can add doctor warnings or automation around stale knowledge.

## 回帰ガード

tests/test_cli/test_mvp_flow.py
