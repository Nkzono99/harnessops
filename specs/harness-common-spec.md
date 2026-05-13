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
- user領域のAgent plugin installは暗黙に実行せず、複数repoでglobal pluginを共有したい場合だけ任意手順として案内する

## 検出優先順位

`hops detect` は次の順序でリポジトリの同一性を解決します。

1. `.harnessops/project.toml`
2. `.harness/manifest.toml`
3. プロバイダ固有マーカー
4. 汎用リポジトリマーカー
