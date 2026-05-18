---
name: hops-global-feedback-issue
description: global/local-state HarnessOps の feedback をサニタイズ済み GitHub Issue 下書きにし、明示確認がある場合だけ issue 作成まで進めるときに使う。
---

Use `uvx --from harnessops hops <command>`; do not rely on `hops` being on PATH.

This skill turns local HarnessOps feedback into an issue-ready artifact while keeping the target repository clean. It also handles incoming GitHub issues as HarnessOps inputs.

## Outbound Issue Draft

Use this when the user asks to "issue化", "GitHub issueにして", "上流に投げる", or "共有できる形にして".

1. Resolve/link local state and validate.

```bash
uvx --from harnessops hops project resolve --json
uvx --from harnessops hops doctor --check-overlay --check-records
```

If not linked:

```bash
uvx --from harnessops hops detect --json
uvx --from harnessops hops project link --storage local --profile <profile-id>
```

2. If the source is only a description, create a failure first.

```bash
uvx --from harnessops hops feedback add-failure ...
uvx --from harnessops hops feedback route --record F0001
```

3. Create an upstream/meta feedback draft when needed.

```bash
uvx --from harnessops hops feedback add --from F0001 --target <target> --summary "<summary>"
```

4. Export a sanitized GitHub Issue draft.

```bash
uvx --from harnessops hops feedback export --target <target> --sanitize --format github-issue
```

5. Show title/body and duplicate candidates without creating a remote issue.

```bash
uvx --from harnessops hops feedback issue create <bundle-path> --repo <owner/repo>
```

6. Create the remote issue only when the user explicitly asks for creation and the body is sanitized.

```bash
uvx --from harnessops hops feedback issue create <bundle-path> --repo <owner/repo> --confirm-create
```

Use `--allow-duplicate` only if the user explicitly accepts duplicate risk.

## Incoming GitHub Issue

Use this when the user asks to inspect or triage issues into HarnessOps.

1. Determine `<owner/repo>` from the user, `git remote -v`, GitHub plugin, or `gh`.
2. If no issue number is given, list open issues and return a triage report.

```bash
gh issue list --repo <owner/repo> --state open --limit 50 --json number,title,labels,updatedAt,url,author
```

3. For a specific issue, inspect details.

```bash
gh issue view <number> --repo <owner/repo> --json number,title,body,labels,comments,createdAt,updatedAt,url,author
```

4. If the current HarnessOps project is upstream/meta lab, import it.

```bash
uvx --from harnessops hops feedback import --issue <number> --repo <owner/repo>
```

5. If the current HarnessOps project is project-side feedback-source, record the observed failure rather than blindly copying issue text.

```bash
uvx --from harnessops hops feedback add-failure ...
uvx --from harnessops hops feedback route --record F0001
```

## Remote Action Rules

- GitHub issue creation requires explicit user authorization or automation prompt authorization.
- Closing, commenting, labeling, or PR creation are not part of this skill unless explicitly authorized.
- If authorization is missing, provide a draft issue/comment and the exact command that would perform the action.
- Never send unsanitized local paths, private terms, or unpublished project context to GitHub.
- HarnessOps records are the source of truth; GitHub issues are external trackers or inputs.
