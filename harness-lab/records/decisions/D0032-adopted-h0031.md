---
id: D0032
record_type: decision
created_at: '2026-05-14T00:11:20+09:00'
status: adopted
source: H0031
evidence:
  summary: ruff check .; pytest -q (92 passed); hops doctor --check-overlay --check-records; hops migrate --check
  guard_path: src/harnessops/core/improvement_dossier.py
---

# D0032: adopted H0031

## 判断

adopted

## 理由

The old records.py module mixed record schemas, IO, indexing, creators, and dossier aggregation. Focused modules make future changes easier to review while retaining the previous import surface through harnessops.core.records.

## 証拠

ruff check .; pytest -q (92 passed); hops doctor --check-overlay --check-records; hops migrate --check

## 回帰リスク

Low-medium: behavior was moved mechanically and the facade preserves old imports; full CLI and record tests passed, but future follow-up should add smaller unit tests for the new modules.

## フォローアップ

変更を昇格する前にこの判断をレビューしてください。

## 回帰ガード

src/harnessops/core/improvement_dossier.py
