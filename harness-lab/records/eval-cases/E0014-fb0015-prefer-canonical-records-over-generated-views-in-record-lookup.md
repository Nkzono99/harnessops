---
id: E0014
record_type: eval_case
created_at: '2026-05-13T02:23:36+09:00'
status: active
capability: record_lookup
failure_class: generated_view_shadowed_record_id
source_feedback: FB0015
---

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
