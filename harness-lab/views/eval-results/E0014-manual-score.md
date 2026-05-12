<!-- harnessops により生成; source records が正本 -->
# 手動評価結果: E0014

送信元: `harness-lab/records/eval-cases/E0014-fb0015-prefer-canonical-records-over-generated-views-in-record-lookup.md`

## スコア

- impact: 4
- mechanism_clarity: 5
- evaluability: 5
- minimality: 5
- regression_risk: 2
- operator_burden: 5
- anti_theater: 5
- maintainability: 4
- privacy_sanitization_risk: 5

## メモ

find_record now searches the canonical record directory implied by known ID prefixes before broad overlay lookup. Regression test reruns eval by ID after an eval result view exists.

## 評価ケーススナップショット

# E0014: FB0015-prefer-canonical-records-over-generated-views-in-record-lookup を評価

## フィクスチャ

フィクスチャディレクトリ: `harness-lab/records/eval-cases/fixtures/E0014`。

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
