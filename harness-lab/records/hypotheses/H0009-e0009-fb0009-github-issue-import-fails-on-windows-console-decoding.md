---
id: H0009
record_type: hypothesis
created_at: '2026-05-13T00:02:45+09:00'
status: proposed
target_capability: github_issue_import
source_eval_case: E0009
---

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
