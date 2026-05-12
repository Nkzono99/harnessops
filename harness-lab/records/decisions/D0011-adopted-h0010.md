---
id: D0011
record_type: decision
created_at: '2026-05-13T01:05:07+09:00'
status: adopted
source: H0010
evidence:
  summary: 'Tests: uv run pytest tests/test_cli/test_mvp_flow.py tests/test_agent_harness_contract.py;
    uv run pytest; uv run ruff check src/harnessops/core/records.py src/harnessops/cli/lab.py
    src/harnessops/core/render.py src/harnessops/core/validation.py src/harnessops/core/agent_bridge.py
    tests/test_cli/test_mvp_flow.py tests/test_agent_harness_contract.py; hops doctor
    --check-overlay --check-records; hops migrate --check. Manual eval: harness-lab/views/eval-results/E0010-manual-score.yml'
  guard_path: tests/test_cli/test_mvp_flow.py
---

# D0011: adopted H0010

## 判断

adopted

## 理由

H0010 の最小実装を採用。標準改善ループを調査・分類・テーマ成熟度・ガード・昇格まで具体化し、CLI と agent skill が自然にその流れを促すようにした。

## 証拠

Tests: uv run pytest tests/test_cli/test_mvp_flow.py tests/test_agent_harness_contract.py; uv run pytest; uv run ruff check src/harnessops/core/records.py src/harnessops/cli/lab.py src/harnessops/core/render.py src/harnessops/core/validation.py src/harnessops/core/agent_bridge.py tests/test_cli/test_mvp_flow.py tests/test_agent_harness_contract.py; hops doctor --check-overlay --check-records; hops migrate --check. Manual eval: harness-lab/views/eval-results/E0010-manual-score.yml

## 回帰リスク

Moderate-low. The new metadata is optional and generated into dossiers, while FB/E/H/D records remain the source of truth. AGENTS.md explicitly allows layout cleanup when migrate/update-harness can carry users forward.

## フォローアップ

Consider adding a dedicated migration if future releases make improvement dossier metadata mandatory or remove older lab structures.

## 回帰ガード

tests/test_cli/test_mvp_flow.py
