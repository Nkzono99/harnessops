<!-- harnessops により生成; source records が正本 -->
# 手動評価結果: E0001

送信元: `harness-lab/records/eval-cases/E0001-fb0001-harnessops-improvements-lacked-lab-trace.md`

## スコア

- impact: 4
- mechanism_clarity: 4
- evaluability: 5
- minimality: 4
- regression_risk: 0
- operator_burden: 0
- anti_theater: 4
- maintainability: 4
- privacy_sanitization_risk: 0

## メモ

CLI tests exercise lab capture and eval conversion. Contract tests assert bridge, packaged skills, release skill, and docs mention hops lab capture. This record captures the previously missing lab trace.

## 評価ケーススナップショット

# E0001: FB0001-harnessops-improvements-lacked-lab-trace を評価

## フィクスチャ

フィクスチャディレクトリ: `harness-lab/records/eval-cases/fixtures/E0001`。

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
