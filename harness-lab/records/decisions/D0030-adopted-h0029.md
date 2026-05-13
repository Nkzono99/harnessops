---
id: D0030
record_type: decision
created_at: '2026-05-13T23:23:04+09:00'
status: adopted
source: H0029
evidence:
  summary: ruff check .; pytest -q (93 passed); hops doctor --check-overlay --check-records; hops migrate --check; git diff --check
  guard_path: src/harnessops/core/upgrade_chain.py
---

# D0030: adopted H0029

## 判断

adopted

## 理由

uvx is now the standard downstream path, so update-harness can use the recorded HarnessOps version in lock.json to run bounded exact-version checkpoints before applying the current runtime. This reduces pressure to keep direct compatibility code forever while preserving an explicit plan/apply path.

## 証拠

ruff check .; pytest -q (93 passed); hops doctor --check-overlay --check-records; hops migrate --check; git diff --check

## 回帰リスク

Medium-low: subprocess uvx chain can fail when a checkpoint is unavailable, but normal update still falls back to direct current refresh when no intermediate checkpoint is available, and tests cover plan, explicit apply, and auto intermediate execution.

## フォローアップ

変更を昇格する前にこの判断をレビューしてください。

## 回帰ガード

src/harnessops/core/upgrade_chain.py
