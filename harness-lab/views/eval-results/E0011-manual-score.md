<!-- harnessops により生成; source records が正本 -->
# 手動評価結果: E0011

送信元: `harness-lab/records/eval-cases/E0011-fb0011-add-meta-hypothesis-scan-harness-for-autonomous-second-order-observations.md`

## スコア

- impact: 5
- mechanism_clarity: 5
- evaluability: 4
- minimality: 4
- regression_risk: 3
- operator_burden: 4
- anti_theater: 4
- maintainability: 4
- privacy_sanitization_risk: 1

## メモ

Designed the meta-hypothesis scan harness: trigger signals, task checkpoints, output levels, capture thresholds, and anti-spam guardrails are documented in design-principles; run-lab skills now instruct agents to run a bounded scan during interruptions, repeated friction, generalization moments, compatibility/migration decisions, evaluation gaps, and external-comparison discoveries. Verified packaged skill contracts, dossier classification/investigation, full pytest, doctor, and migrate.

## 評価ケーススナップショット

# E0011: FB0011-add-meta-hypothesis-scan-harness-for-autonomous-second-order-observations を評価

## フィクスチャ

フィクスチャディレクトリ: `harness-lab/records/eval-cases/fixtures/E0011`。

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
