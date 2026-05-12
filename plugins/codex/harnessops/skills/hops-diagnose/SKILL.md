---
name: hops-diagnose
description: リポジトリが HarnessOps にリンクされているか、オーバーレイが健全かを確認するときに使う。
---

`hops doctor --check-overlay` を実行する。リポジトリがリンクされていなければ、`hops detect` を実行して `hops init --profile <detected-profile>` を提案する。
