---
name: hops-export-feedback
description: サニタイズ済みのプロジェクト側フィードバックをターゲットハーネスまたは HarnessOps へエクスポートするときに使う。
---

`hops feedback export --target <target> --sanitize` を実行する。リモートIssueやプルリクエストは作成しない。

共有前に、エクスポートされたバンドルにローカルパス、非公開語、未公開研究の詳細が残っていないか確認する。
