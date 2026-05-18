---
name: hops-global-add-failure
description: 普通のrepoを汚さず、global/local-state HarnessOps に失敗、摩擦、ローカル回避策、上流フィードバック候補を記録するときに使う。
---

Use `uvx --from harnessops hops <command>`; do not rely on `hops` being on PATH.

This skill is for global/local-state usage. Keep the target repository clean unless the user explicitly asks for repo-local HarnessOps files.

## Workflow

1. Resolve the project.

```bash
uvx --from harnessops hops project resolve --json
```

2. If not linked, detect and create a local-state link.

```bash
uvx --from harnessops hops detect --json
uvx --from harnessops hops project link --storage local --profile <profile-id>
```

Use `generic-code` only when detection does not return a better profile and the user did not specify one.

3. Validate.

```bash
uvx --from harnessops hops doctor --check-overlay --check-records
```

4. Gather a concise record: title, context, what happened, why it matters, desired behavior, local workaround, target, and privacy risks.

5. Create the failure record.

```bash
uvx --from harnessops hops feedback add-failure \
  --title "<title>" \
  --target "<target>" \
  --context "<context>" \
  --what-happened "<what happened>" \
  --why-matters "<why it matters>" \
  --desired-behavior "<desired behavior>" \
  --local-workaround "<local workaround>"
```

6. Route it when disposition is unclear or the user asks whether it should become upstream/meta feedback.

```bash
uvx --from harnessops hops feedback route --record F0001
```

7. If it is upstream/meta feedback, suggest `hops-global-feedback-issue` or export with sanitize.

## Rules

- Do not create `.harnessops/`, `harness-feedback/`, `harness-lab/`, or `.agents/skills/` in the target repo.
- Project-specific research direction belongs in the project `research/` or `notes/`, not in HarnessOps feedback.
- Do not include raw local paths, private terms, or unpublished project context in issue drafts or remote comments.
