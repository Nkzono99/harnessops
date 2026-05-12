---
id: D0009
record_type: decision
created_at: '2026-05-13T00:32:27+09:00'
status: adopted
source: H0008
evidence:
  summary: "Tests: uv run pytest tests/test_cli/test_safety.py -k 'lab_issue or feedback_issue_create_writes_back';
    uv run pytest tests/test_cli/test_mvp_flow.py tests/test_cli/test_safety.py tests/test_agent_harness_contract.py;
    uv run pytest; uv run ruff check src/harnessops/cli/lab.py tests/test_cli/test_safety.py;
    hops lab issue --help; hops doctor --check-overlay --check-records; hops migrate
    --check. Manual eval: harness-lab/views/eval-results/E0008-manual-score.yml"
  guard_path: tests/test_cli/test_safety.py
---

# D0009: adopted H0008

## 判断

adopted

## 理由

H0008 の最小実装を採用。lab-first record から sanitized draft/create へ進む first-class command を追加し、remote create は重複確認と --confirm-create の下だけにした。

## 証拠

Tests: uv run pytest tests/test_cli/test_safety.py -k 'lab_issue or feedback_issue_create_writes_back'; uv run pytest tests/test_cli/test_mvp_flow.py tests/test_cli/test_safety.py tests/test_agent_harness_contract.py; uv run pytest; uv run ruff check src/harnessops/cli/lab.py tests/test_cli/test_safety.py; hops lab issue --help; hops doctor --check-overlay --check-records; hops migrate --check. Manual eval: harness-lab/views/eval-results/E0008-manual-score.yml

## 回帰リスク

Moderate. The command reuses existing GitHub issue helpers and sanitizer, but imports private helper functions from feedback CLI; future cleanup can move them to a shared GitHub issue bridge module.

## フォローアップ

Consider provider abstraction or shared helper extraction if more lab issue workflows are added.

## 回帰ガード

tests/test_cli/test_safety.py
