---
id: FB0017
record_type: imported_feedback
created_at: '2026-05-13T02:52:51+09:00'
status: triaged
source:
  type: local-capture
  original_id: https://claude.com/blog/new-in-claude-managed-agents
  source_project: harnessops
classification:
  capability: lab_memory_compaction
  failure_class: record_sprawl_without_knowledge_consolidation
links:
  eval_case:
  issue_url: https://claude.com/blog/new-in-claude-managed-agents
---

# FB0017: Compact lab records into mutable knowledge

## 概要

As harness-lab grows, append-only records and generated dossiers will become too large to scan. The lab needs a compaction path that preserves canonical records while updating a smaller knowledge layer for reusable lessons, contradictions, guards, and promotion patterns.

## 再現

Accumulate feedback, eval cases, hypotheses, decisions, manual scores, and dossiers until reviewing harness-lab requires reading many files instead of consulting a compiled knowledge surface.

## 期待する上流変更

Provide a first-class lab compaction command that checks size thresholds, compiles source-linked mutable knowledge files, and leaves canonical records intact for audit and regeneration.
