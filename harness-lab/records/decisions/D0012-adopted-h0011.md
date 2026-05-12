---
id: D0012
record_type: decision
created_at: '2026-05-13T01:37:49+09:00'
status: adopted
source: H0011
evidence:
  summary: "Tests: uv run pytest tests/test_agent_harness_contract.py -k 'lab_capture
    or packaged_agent_assets'; uv run pytest tests/test_cli/test_mvp_flow.py -k lab_dossier;
    uv run pytest; uv run ruff check tests/test_agent_harness_contract.py src/harnessops/core/records.py
    src/harnessops/cli/lab.py src/harnessops/core/render.py src/harnessops/core/validation.py;
    hops doctor --check-overlay --check-records; hops migrate --check. Manual eval:
    harness-lab/views/eval-results/E0011-manual-score.yml"
  guard_path: tests/test_agent_harness_contract.py
---

# D0012: adopted H0011

## 判断

adopted

## 理由

H0011 を採用。作業中の二階観測を自律的に拾うため、発火シグナル、チェックポイント、出力レベル、ノイズ抑制を定義し、run-lab skill に標準手順として組み込んだ。

## 証拠

Tests: uv run pytest tests/test_agent_harness_contract.py -k 'lab_capture or packaged_agent_assets'; uv run pytest tests/test_cli/test_mvp_flow.py -k lab_dossier; uv run pytest; uv run ruff check tests/test_agent_harness_contract.py src/harnessops/core/records.py src/harnessops/cli/lab.py src/harnessops/core/render.py src/harnessops/core/validation.py; hops doctor --check-overlay --check-records; hops migrate --check. Manual eval: harness-lab/views/eval-results/E0011-manual-score.yml

## 回帰リスク

Moderate-low. The scan is guidance with bounded output levels, so it should improve capture of high-signal meta observations without requiring a new mandatory record for every thought.

## フォローアップ

Evaluate future sessions for whether agents actually create investigate/classify/capture entries without user prompting when generalizable observations appear.

## 回帰ガード

tests/test_agent_harness_contract.py
