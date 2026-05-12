---
id: H0007
record_type: hypothesis
created_at: '2026-05-13T00:01:22+09:00'
status: proposed
target_capability: unclassified
source_eval_case: E0007
---

# H0007: E0007-fb0007-simplify-harness-lab-around-per-improvement-dossiers の仮説

## 仮説

普通の harness 改善を one improvement dossier に集約し、typed records は派生または advanced layer にすると、日常運用の記録コストを下げながら評価記憶を保てる。

## メカニズム

harness-lab/improvements/IMPxxxx を living source of truth にし、status、source observation、hypothesis、eval plan、evidence、links、decision log を同一ファイルに置き、views はそこから生成する。

## 最小実装

新規 dossier 作成/更新コマンドを追加し、既存 records/* は互換読み取りまたは migration path として残す。

## 代替案: 削除または統合

現在の FB/E/H/X/D 正規化レイアウトを維持し、views と docs だけで見通しを改善する。

## 期待される利点

agent とユーザーが一つのファイルを開けば改善履歴を追えるようになり、lab が戻ってくる場所として機能しやすくなる。

## 想定される欠点

既存の正規化レコード、score trajectory、decision workflow との対応関係が曖昧になる可能性がある。

## 評価計画

既存 issue #5〜#8 を dossier 形式で表現できるか試し、backlog/imported-feedback/score views と migration docs が破綻しないことを確認する。

## 中止基準

dossier が自由記述ノートになり、評価ケースや採用判断の証拠を機械的に追えなくなる場合は採用しない。
