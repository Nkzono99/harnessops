<!-- harnessops により生成; source records が正本 -->
# 手動評価結果: E0006

送信元: `harness-lab/records/eval-cases/E0006-fb0006-make-update-harness-conflict-aware-for-agent-bridge-files.md`

## スコア

- impact: 4
- mechanism_clarity: 5
- evaluability: 5
- minimality: 4
- regression_risk: 3
- operator_burden: 4
- anti_theater: 5
- maintainability: 4
- privacy_sanitization_risk: 1

## メモ

Implemented conflict-aware agent bridge refresh: managed bridge hashes are stored in lock metadata; unmodified stale files update automatically, local edits produce .new files, --force-agent-bridge overwrites explicitly, and JSON/text output reports checked, updated, unchanged, conflicted, and written_new paths. Verified with focused tests, full pytest, ruff, doctor, and migrate.

## 評価ケーススナップショット

# E0006: FB0006-make-update-harness-conflict-aware-for-agent-bridge-files を評価

## フィクスチャ

フィクスチャディレクトリ: `harness-lab/records/eval-cases/fixtures/E0006`。

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
