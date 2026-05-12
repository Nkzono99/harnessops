<!-- harnessops により生成; source records が正本 -->
# 手動評価結果: E0012

送信元: `harness-lab/records/eval-cases/E0012-fb0012-add-manual-meta-improvement-research-skill.md`

## スコア

- impact: 4
- mechanism_clarity: 4
- evaluability: 4
- minimality: 4
- regression_risk: 3
- operator_burden: 3
- anti_theater: 4
- maintainability: 4
- privacy_sanitization_risk: 4

## メモ

The skill is distinct from the in-task meta scan, lab-routed, package-tested, and privacy-aware. Risk is moderate skill surface area, guarded by explicit trigger criteria and packaging contract tests.

## 評価ケーススナップショット

# E0012: FB0012-add-manual-meta-improvement-research-skill を評価

## フィクスチャ

フィクスチャディレクトリ: `harness-lab/records/eval-cases/fixtures/E0012`。

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
