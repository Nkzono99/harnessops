---
id: FB0009
record_type: imported_feedback
created_at: '2026-05-13T00:02:19+09:00'
status: triaged
source:
  type: local-capture
  original_id: local-session-2026-05-12-issue-triage
  source_project: harnessops
classification:
  capability: github_issue_import
  failure_class: unicode_decode_failure
links:
  eval_case:
  issue_url:
---

# FB0009: GitHub issue import fails on Windows console decoding

## 概要

hops feedback import --issue 7 --repo Nkzono99/harnessops crashed on Windows cp932 decoding while reading gh JSON for a Unicode issue body; setting PYTHONUTF8=1 allowed the import to complete.

## 再現

On Windows PowerShell with the default cp932 locale, run uv run --with-editable . hops feedback import --issue 7 --repo Nkzono99/harnessops. The subprocess reader raises UnicodeDecodeError and json.loads receives None.

## 期待する上流変更

Decode gh issue JSON as UTF-8 explicitly, or capture bytes and decode UTF-8, then add coverage for Unicode issue bodies on Windows.
