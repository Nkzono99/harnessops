<!-- harnessops により生成; source records が正本 -->
# 手動評価結果: E0037

送信元: `harness-lab/records/eval-cases/E0037-fb0047-cli-surface-needs-canonical-grouped-commands.md`

## スコア

- impact: 3
- mechanism_clarity: 4
- evaluability: 4
- minimality: 4
- regression_risk: 3
- operator_burden: 4
- anti_theater: 4
- maintainability: 3
- privacy_sanitization_risk: 5

## メモ

Implemented read-time canonicalization for research-scan queue next_command values and added regression coverage in tests/test_cli/test_lab_usage.py; focused pytest passed. This validates the stale queue-command part of FB0047, but not the full command-surface audit for all aliases.

## 評価ケース

- capability: cli_ergonomics
- failure_class: command_surface_sprawl
- source_feedback: FB0047
