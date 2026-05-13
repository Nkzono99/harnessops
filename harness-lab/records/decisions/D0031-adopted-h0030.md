---
id: D0031
record_type: decision
created_at: '2026-05-13T23:51:48+09:00'
status: adopted
source: H0030
evidence:
  summary: ruff check .; pytest -q (92 passed); hops doctor --check-overlay --check-records; hops migrate --check
  guard_path: src/harnessops/cli/agent.py
---

# D0031: adopted H0030

## 判断

adopted

## 理由

Repo-local skills are now the standard agent path, so root plugin mirrors and user plugin install support add maintenance surface without improving the current workflow. Small shared helpers reduce duplication without changing record or managed-file behavior.

## 証拠

ruff check .; pytest -q (92 passed); hops doctor --check-overlay --check-records; hops migrate --check

## 回帰リスク

Medium-low: removes optional plugin UX, but repo-local skill generation and packaged skill assets remain covered by tests; experiment record reading remains compatible but experiments are no longer required in the default lab layout.

## フォローアップ

変更を昇格する前にこの判断をレビューしてください。

## 回帰ガード

src/harnessops/cli/agent.py
