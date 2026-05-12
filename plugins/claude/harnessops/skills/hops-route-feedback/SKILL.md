---
name: hops-route-feedback
description: HarnessOps フィードバックを project、target、meta、protocol、external、private のdispositionへ分類するときに使う。
---

`hops doctor --check-overlay` の後に `hops route --record <id>` を実行する。

1つのイベントにプロジェクト発展とハーネス不足の両方が含まれる場合は、別々のレコードに分割する。プロジェクト固有の文脈を上流化しない。
