<!-- harnessops により生成; source records が正本 -->
# 手動評価結果: E0013

送信元: `harness-lab/records/eval-cases/E0013-fb0014-prevent-duplicate-improvement-dossiers-from-concurrent-lab-commands.md`

## スコア

- impact: 4
- mechanism_clarity: 5
- evaluability: 5
- minimality: 4
- regression_risk: 3
- operator_burden: 4
- anti_theater: 5
- maintainability: 4
- privacy_sanitization_risk: 5

## メモ

Implemented source_feedback-level locking for dossier creation, doctor validation for duplicate improvement dossier source_feedback values, visible evidence_ref rendering for investigation notes, LF-stable generated records, and canonical record lookup so generated views do not shadow eval cases.

## 評価ケーススナップショット

# E0013: FB0014-prevent-duplicate-improvement-dossiers-from-concurrent-lab-commands を評価

## フィクスチャ

フィクスチャディレクトリ: `harness-lab/records/eval-cases/fixtures/E0013`。

## タスク

この失敗を防ぐべき挙動を記述してください。

## 期待される挙動

ターゲットハーネスが、非公開プロジェクト文脈を漏らさずに失敗クラスを扱います。

## 合格基準

- 失敗条件が検出または防止される。
- 提案される挙動が上流メンテナにとって実行可能である。
- 非公開プロジェクト詳細を必要としない。

## 不合格基準

- 失敗を見逃す。
- 再現に非公開文脈が必要になる。
