---
id: IMP0005
record_type: improvement_dossier
created_at: '2026-05-13T00:35:12+09:00'
updated_at: '2026-05-13T02:42:04+09:00'
status: adopted
source_type: observation
scope: harnessops-core
maturity: adopted
relation: new
promotion_level: target-lab-case
source_feedback: FB0009
eval_cases:
- E0009
hypotheses:
- H0009
decisions:
- D0010
classification:
  capability: github_issue_import
  failure_class: unicode_decode_failure
guard:
  status: not-defined
  path:
investigation: []
links:
  issue_url:
---

# IMP0005: FB0009: GitHub issue import fails on Windows console decoding

## Status

- status: adopted
- maturity: adopted
- source_type: observation
- scope: harnessops-core
- relation: new
- promotion_level: target-lab-case
- source_feedback: `FB0009`
- linked_records: `FB0009`, `E0009`, `H0009`, `D0010`

## Source Observation

Source: `harness-lab/records/feedback/FB0009-github-issue-import-fails-on-windows-console-decoding.md`

# FB0009: GitHub issue import fails on Windows console decoding

## 概要

hops feedback import --issue 7 --repo Nkzono99/harnessops crashed on Windows cp932 decoding while reading gh JSON for a Unicode issue body; setting PYTHONUTF8=1 allowed the import to complete.

## 再現

On Windows PowerShell with the default cp932 locale, run uv run --with-editable . hops feedback import --issue 7 --repo Nkzono99/harnessops. The subprocess reader raises UnicodeDecodeError and json.loads receives None.

## 期待する上流変更

Decode gh issue JSON as UTF-8 explicitly, or capture bytes and decode UTF-8, then add coverage for Unicode issue bodies on Windows.

## Target Capability

- capability: github_issue_import
- failure_class: unicode_decode_failure

## Investigation

調査メモはまだありません。

## Evaluation

### E0009: E0009: FB0009-github-issue-import-fails-on-windows-console-decoding を評価


- source: `harness-lab/records/eval-cases/E0009-fb0009-github-issue-import-fails-on-windows-console-decoding.md`

- capability: github_issue_import

- failure_class: unicode_decode_failure

- manual_eval_yml: `harness-lab/views/eval-results/E0009-manual-score.yml`
- manual_eval_md: `harness-lab/views/eval-results/E0009-manual-score.md`
- scores: impact=3, mechanism_clarity=5, evaluability=5, minimality=5, regression_risk=2, operator_burden=5, anti_theater=5, maintainability=5, privacy_sanitization_risk=1
- notes: Implemented explicit UTF-8 decoding for gh issue view during feedback import, with replacement on invalid bytes and TypeError fallback handling. Regression test now imports Unicode Japanese issue body/comment and asserts encoding=utf-8 is used. Verified with focused ruff/test, full pytest, doctor, and migrate.


## Hypotheses

### H0009: H0009: E0009-fb0009-github-issue-import-fails-on-windows-console-decoding の仮説


Source: `harness-lab/records/hypotheses/H0009-e0009-fb0009-github-issue-import-fails-on-windows-console-decoding.md`


# H0009: E0009-fb0009-github-issue-import-fails-on-windows-console-decoding の仮説

## 仮説

gh issue view の JSON 出力を UTF-8 として明示デコードすれば、Windows cp932 環境でも Unicode を含む issue body/comment を落とさず import できる。

## メカニズム

_load_github_issue の subprocess.run で encoding=utf-8 を指定するか、text=False で bytes を受けて UTF-8 decode し、decode 失敗時は fallback source に安全に戻す。

## 最小実装

feedback import --issue の gh 呼び出しに explicit UTF-8 decode と TypeError を含む fallback handling を追加し、Unicode issue fixture で回帰テストする。

## 代替案: 削除または統合

利用者に PYTHONUTF8=1 を要求する運用回避に留める。

## 期待される利点

日本語や記号を含む GitHub issue を Windows から安定して HarnessOps lab に取り込める。

## 想定される欠点

gh 出力が UTF-8 以外になる特殊環境では fallback 判定を確認する必要がある。

## 評価計画

cp932 相当の Windows locale を想定した test で Unicode body を返す gh stub を import し、record に本文が保存されることを確認する。

## 中止基準

明示 UTF-8 decode が gh の実際の出力仕様と合わない、または fallback が issue metadata を silently 欠落させる場合は採用しない。


## Evidence

`harness-lab/views/eval-results/E0009-manual-score.md`

## Guard

- status: not-defined
- path: None

## Links

- issue_url: 未設定

## Open Questions And Next Action

次の実装または評価ステップは、この dossier と紐づく正規化レコードを更新してから再生成してください。

## Decision Log

### D0010: D0010: adopted H0009


Source: `harness-lab/records/decisions/D0010-adopted-h0009.md`


# D0010: adopted H0009

## 判断

adopted

## 理由

H0009 の最小修正を採用。gh issue view の JSON を UTF-8 として明示的に読み、Windows cp932 既定環境でも Unicode issue import が壊れないようにした。

## 証拠

Tests: uv run pytest tests/test_cli/test_mvp_flow.py -k feedback_import_issue_captures_github_context; uv run pytest; uv run ruff check src/harnessops/cli/feedback.py tests/test_cli/test_mvp_flow.py; hops doctor --check-overlay --check-records; hops migrate --check. Manual eval: harness-lab/views/eval-results/E0009-manual-score.yml

## 回帰リスク

Low. The change is limited to the gh issue view subprocess call used by feedback import; invalid UTF-8 bytes are replaced and existing fallback behavior is retained for malformed output.

## フォローアップ

Consider moving all gh subprocess calls to a shared UTF-8 wrapper.

## 回帰ガード

tests/test_cli/test_mvp_flow.py
