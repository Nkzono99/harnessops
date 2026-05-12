<!-- harnessops により生成; source records が正本 -->
# 手動評価結果: E0004

送信元: `harness-lab/records/eval-cases/E0004-fb0004-github-issue-3.md`

## スコア

- impact: 5
- mechanism_clarity: 0
- evaluability: 0
- minimality: 0
- regression_risk: 0
- operator_burden: 0
- anti_theater: 5
- maintainability: 0
- privacy_sanitization_risk: 0

## メモ

Implemented regression coverage for dynamic imported-feedback views and fixed update-harness lock hashes to use file bytes on Windows; doctor reports ok after update-harness.

## 評価ケーススナップショット

# E0004: FB0004-github-issue-3 を評価

## フィクスチャ

フィクスチャディレクトリ: `harness-lab/records/eval-cases/fixtures/E0004`。

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
