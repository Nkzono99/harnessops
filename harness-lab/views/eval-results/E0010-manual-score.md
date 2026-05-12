<!-- harnessops により生成; source records が正本 -->
# 手動評価結果: E0010

送信元: `harness-lab/records/eval-cases/E0010-fb0010-redesign-standard-improvement-loop-around-investigation-and-themes.md`

## スコア

- impact: 4
- mechanism_clarity: 5
- evaluability: 5
- minimality: 4
- regression_risk: 3
- operator_burden: 4
- anti_theater: 4
- maintainability: 4
- privacy_sanitization_risk: 1

## メモ

Redesigned the standard improvement loop around explicit observation, investigation, recording, classification/routing, hypothesis, evaluation design, decision, application, guard, and promotion. Added improvement theme metadata plus lab investigate/classify commands, extended dossier rendering and views, updated agent skills so the flow is natural, and documented that backward compatibility can be cut when migrate/update-harness provides a migration path. Verified with focused tests, full pytest, doctor, and migrate.

## 評価ケーススナップショット

# E0010: FB0010-redesign-standard-improvement-loop-around-investigation-and-themes を評価

## フィクスチャ

フィクスチャディレクトリ: `harness-lab/records/eval-cases/fixtures/E0010`。

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
