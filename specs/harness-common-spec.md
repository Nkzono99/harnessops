# Harness共通仕様

`.harness/manifest.toml` はプロバイダ中立のマーカーファイルです。HarnessOps は検出とプロファイルヒントに使いますが、このファイル自体は HarnessOps 固有ではありません。

## 必須形状

```toml
schema_version = "0.1"

[harness]
provider = "runops"
kind = "generated-project"
version = "0.9.0"

[commands]
doctor = "runo doctor"
update = "runo update-harness"
migrate = "runo migrate"
feedback = "runo feedback"
version = "runo version"

[harnessops]
recommended_profile = "runops-project"
```

## セマンティクス

| フィールド | 必須 | 意味 |
|---|---:|---|
| `schema_version` | はい | 共通マニフェストのスキーマバージョン。 |
| `harness.provider` | はい | 上流ハーネスまたはツール名。 |
| `harness.kind` | はい | `generated-project`、`paper-project`、`upstream`、`core` など。 |
| `harness.version` | 推奨 | プロバイダバージョン。 |
| `commands.*` | 任意 | プロバイダコマンド契約。 |
| `harnessops.recommended_profile` | 任意 | HarnessOps 検出ヒント。 |

## HarnessOps lifecycle連携

target harness の `init`、`setup`、`update-harness` などは、HarnessOps の管理対象状態を直接書かず、`uvx --from harnessops hops` を呼び出します。

- project repository 生成後: `uvx --from harnessops hops init --profile <target-project-profile>` と `uvx --from harnessops hops doctor --check-overlay --check-records`
- target repository setup時: `uvx --from harnessops hops init --profile <target-upstream-profile>` と `uvx --from harnessops hops doctor --check-overlay --check-records`
- update時: `uvx --refresh-package harnessops --from harnessops hops update-harness`
- `hops update-harness` は `hops doctor --check-overlay --check-records` と `hops migrate --check` 相当の確認を含む
- lock の `harnessops_version` が古い場合、`hops update-harness` は PyPI checkpoint 版を `uvx --from harnessops==<version> hops update-harness` で順に適用してから現在版の更新を続ける
- 段階更新の事前確認: `uvx --refresh-package harnessops --from harnessops hops update-harness --plan-upgrade`
- migration適用時: 人間確認または明示フラグ付きで `uvx --from harnessops hops update-harness --apply-migrations` または `uvx --from harnessops hops migrate --apply`
- 編集済みmanaged fileは上書きせず、runops と同様に `<path>.new` を作る
- repo-local skill展開は、明示オプションで `uvx --from harnessops hops agent bridge --codex` または `uvx --from harnessops hops init --with-agent-bridge` を呼んでよい
- repo-local bridge と skill 展開は overlay mode に合わせる。`feedback-source` / `local-and-feedback` は feedback capture/export と lifecycle 系に絞り、lab/eval/propose/decide は `upstream-lab` / `meta-lab` にだけ出す
- target/meta repo では GitHub Flow skill を既定で配布し、`uvx --from harnessops hops github-flow preflight/publish/pr/merge` で automation branch、PR、required checks 後の merge を標準化する
- project repo では GitHub Flow skill を通常配布しない。target/meta repo でも `.harnessops/project.toml` の `[github_flow] enabled = false` または `--no-github-flow` で配布を止められる
- 普通のrepoを汚さない開発時利用では `uvx --from harnessops hops project link --storage local` と global Codex plugin を使う。target/project repo に状態を含める運用では repo-local skill を使う

## 解決と検出の優先順位

`hops project resolve` は次の順序で HarnessOps project を解決します。

1. `.harnessops/project.toml`
2. global registry の `~/.harnessops/registry.toml`

未リンク時の `hops detect` は `.harness/manifest.toml` や repository markers から推奨 profile を推定します。
3. プロバイダ固有マーカー
4. 汎用リポジトリマーカー
