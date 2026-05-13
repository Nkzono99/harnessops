---
id: D0026
record_type: decision
created_at: '2026-05-13T18:53:01+09:00'
status: adopted
source: H0025
evidence:
  summary: Added hops-open-meta-scan across repo-local, Codex/Claude plugins, and packaged assets; updated hops-research-improvements and docs; uv run pytest tests/test_agent_harness_contract.py; uv run ruff check tests/test_agent_harness_contract.py; hops doctor --check-overlay --check-records; manual eval E0025.
  guard_path: tests/test_agent_harness_contract.py
---

# D0026: adopted H0025

## 判断

adopted

## 理由

The implementation separates divergent meta-idea generation from evidence/routing workflow while preserving HarnessOps safety and packaging guarantees.

## 証拠

Added hops-open-meta-scan across repo-local, Codex/Claude plugins, and packaged assets; updated hops-research-improvements and docs; uv run pytest tests/test_agent_harness_contract.py; uv run ruff check tests/test_agent_harness_contract.py; hops doctor --check-overlay --check-records; manual eval E0025.

## 回帰リスク

Low to moderate. A new skill adds trigger surface, but it explicitly avoids default lab writes and is paired with downstream research routing.

## フォローアップ

Forward-test the open scan against a broad meta-improvement prompt and compare novelty/diversity with the research routing skill.

## 回帰ガード

tests/test_agent_harness_contract.py
