import json
import subprocess

from typer.testing import CliRunner

from harnessops.cli import feedback as feedback_cli
from harnessops.cli.main import app
from harnessops.core.records import read_record


runner = CliRunner()


def test_init_refuses_to_overwrite_user_edited_generated_file(
    copy_fixture, monkeypatch
):
    root = copy_fixture("runops-project-minimal")
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init", "--profile", "runops-project"]).exit_code == 0
    readme = root / "harness-feedback/README.md"
    readme.write_text("# human edit\n", encoding="utf-8")

    result = runner.invoke(app, ["init", "--profile", "runops-project"])

    assert result.exit_code == 2
    assert readme.read_text(encoding="utf-8") == "# human edit\n"


def test_feedback_export_refuses_unsanitized_by_default(copy_fixture, monkeypatch):
    root = copy_fixture("runops-project-minimal")
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init", "--profile", "runops-project"]).exit_code == 0
    assert (
        runner.invoke(
            app,
            ["add-failure", "--title", "Harness update missed", "--target", "runops"],
        ).exit_code
        == 0
    )

    result = runner.invoke(app, ["feedback", "export", "--target", "runops"])

    assert result.exit_code == 1
    assert "未サニタイズエクスポートは拒否" in result.output


def test_github_issue_draft_requires_strict_sanitize(copy_fixture, monkeypatch):
    root = copy_fixture("runops-project-minimal")
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init", "--profile", "runops-project"]).exit_code == 0
    assert (
        runner.invoke(
            app,
            [
                "add-failure",
                "--title",
                "Harness update missed",
                "--target",
                "runops",
                "--context",
                f"local path leaked from {root}/private/notes.md",
            ],
        ).exit_code
        == 0
    )

    unsanitized = runner.invoke(
        app,
        [
            "feedback",
            "export",
            "--target",
            "runops",
            "--format",
            "github-issue",
            "--allow-private",
        ],
    )
    assert unsanitized.exit_code == 1
    assert "GitHub Issue下書きは --sanitize が必須" in unsanitized.output

    allow_private = runner.invoke(
        app,
        [
            "feedback",
            "export",
            "--target",
            "runops",
            "--format",
            "github-issue",
            "--sanitize",
            "--allow-private",
        ],
    )
    assert allow_private.exit_code == 1
    assert "allow-private とは併用できません" in allow_private.output

    sanitized = runner.invoke(
        app,
        [
            "feedback",
            "export",
            "--target",
            "runops",
            "--format",
            "github-issue",
            "--sanitize",
        ],
    )
    assert sanitized.exit_code == 0
    draft = root / sanitized.output.strip()
    draft_text = draft.read_text(encoding="utf-8")
    assert "## Issue下書き" in draft_text
    assert "HarnessOps はリモートIssueを自動作成しません" in draft_text
    assert str(root) not in draft_text


def test_feedback_issue_create_previews_and_searches_without_confirm(
    copy_fixture, monkeypatch
):
    root = copy_fixture("runops-project-minimal")
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init", "--profile", "runops-project"]).exit_code == 0
    assert (
        runner.invoke(
            app,
            ["add-failure", "--title", "Harness update missed", "--target", "runops"],
        ).exit_code
        == 0
    )
    assert (
        runner.invoke(
            app,
            [
                "add-feedback",
                "--from",
                "F0001",
                "--target",
                "runops",
                "--summary",
                "GitHub issue helper feedback",
            ],
        ).exit_code
        == 0
    )
    exported = runner.invoke(
        app,
        [
            "feedback",
            "export",
            "--target",
            "runops",
            "--sanitize",
            "--format",
            "github-issue",
        ],
    )
    assert exported.exit_code == 0
    calls = []

    def fake_run(args, check, capture_output, text):
        calls.append(args)
        assert check is True
        assert capture_output is True
        assert text is True
        if args[:3] == ["gh", "issue", "list"]:
            payload = [
                {
                    "number": 7,
                    "title": "runops へのフィードバック",
                    "url": "https://github.com/example/repo/issues/7",
                    "state": "OPEN",
                }
            ]
            return subprocess.CompletedProcess(
                args=args, returncode=0, stdout=json.dumps(payload), stderr=""
            )
        raise AssertionError(f"unexpected gh call: {args}")

    monkeypatch.setattr(feedback_cli.subprocess, "run", fake_run)

    result = runner.invoke(
        app,
        [
            "feedback",
            "issue",
            "create",
            exported.output.strip(),
            "--repo",
            "example/repo",
        ],
    )

    assert result.exit_code == 0
    assert "Issue title:" in result.output
    assert "Issue body:" in result.output
    assert "重複候補" in result.output
    assert "https://github.com/example/repo/issues/7" in result.output
    assert "リモートIssueは作成していません" in result.output
    assert not any(args[:3] == ["gh", "issue", "create"] for args in calls)


def test_feedback_issue_create_requires_sanitized_issue_bundle(
    copy_fixture, monkeypatch
):
    root = copy_fixture("runops-project-minimal")
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init", "--profile", "runops-project"]).exit_code == 0
    assert (
        runner.invoke(
            app,
            ["add-failure", "--title", "Harness update missed", "--target", "runops"],
        ).exit_code
        == 0
    )
    exported = runner.invoke(
        app,
        ["feedback", "export", "--target", "runops", "--sanitize"],
    )
    assert exported.exit_code == 0

    result = runner.invoke(
        app,
        [
            "feedback",
            "issue",
            "create",
            exported.output.strip(),
            "--repo",
            "example/repo",
        ],
    )

    assert result.exit_code == 1
    assert "--format github-issue" in result.output


def test_feedback_issue_create_rejects_remaining_private_markers(
    copy_fixture, monkeypatch
):
    root = copy_fixture("runops-project-minimal")
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init", "--profile", "runops-project"]).exit_code == 0
    assert (
        runner.invoke(
            app,
            ["add-failure", "--title", "Harness update missed", "--target", "runops"],
        ).exit_code
        == 0
    )
    exported = runner.invoke(
        app,
        [
            "feedback",
            "export",
            "--target",
            "runops",
            "--sanitize",
            "--format",
            "github-issue",
        ],
    )
    assert exported.exit_code == 0
    draft = root / exported.output.strip()
    draft.write_text(
        draft.read_text(encoding="utf-8") + f"\nleaked path: {root}/private.md\n",
        encoding="utf-8",
    )

    result = runner.invoke(
        app,
        [
            "feedback",
            "issue",
            "create",
            exported.output.strip(),
            "--repo",
            "example/repo",
        ],
    )

    assert result.exit_code == 1
    assert "再サニタイズが必要" in result.output


def test_feedback_issue_create_writes_fallback_draft_when_gh_unavailable(
    copy_fixture, monkeypatch
):
    root = copy_fixture("runops-project-minimal")
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init", "--profile", "runops-project"]).exit_code == 0
    assert (
        runner.invoke(
            app,
            ["add-failure", "--title", "Harness update missed", "--target", "runops"],
        ).exit_code
        == 0
    )
    exported = runner.invoke(
        app,
        [
            "feedback",
            "export",
            "--target",
            "runops",
            "--sanitize",
            "--format",
            "github-issue",
        ],
    )
    assert exported.exit_code == 0

    def fake_run(args, check, capture_output, text):
        raise FileNotFoundError("gh")

    monkeypatch.setattr(feedback_cli.subprocess, "run", fake_run)

    result = runner.invoke(
        app,
        [
            "feedback",
            "issue",
            "create",
            exported.output.strip(),
            "--repo",
            "example/repo",
        ],
    )

    assert result.exit_code == 0
    assert "Markdown下書きを書きました" in result.output
    drafts = list(
        (root / "harness-feedback/views/exported-feedback").glob(
            "*github-issue-draft.md"
        )
    )
    assert len(drafts) == 1
    assert "HarnessOps はリモートIssueを自動作成しません" in drafts[0].read_text(
        encoding="utf-8"
    )


def test_feedback_issue_create_writes_back_created_issue_url(copy_fixture, monkeypatch):
    root = copy_fixture("runops-project-minimal")
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init", "--profile", "runops-project"]).exit_code == 0
    assert (
        runner.invoke(
            app,
            ["add-failure", "--title", "Harness update missed", "--target", "runops"],
        ).exit_code
        == 0
    )
    feedback = runner.invoke(
        app,
        [
            "add-feedback",
            "--from",
            "F0001",
            "--target",
            "runops",
            "--summary",
            "GitHub issue helper feedback",
        ],
    )
    assert feedback.exit_code == 0
    feedback_path = root / feedback.output.strip()
    exported = runner.invoke(
        app,
        [
            "feedback",
            "export",
            "--target",
            "runops",
            "--sanitize",
            "--format",
            "github-issue",
        ],
    )
    assert exported.exit_code == 0

    def fake_run(args, check, capture_output, text):
        assert check is True
        assert capture_output is True
        assert text is True
        if args[:3] == ["gh", "issue", "list"]:
            return subprocess.CompletedProcess(
                args=args, returncode=0, stdout="[]", stderr=""
            )
        if args[:3] == ["gh", "issue", "create"]:
            return subprocess.CompletedProcess(
                args=args,
                returncode=0,
                stdout="https://github.com/example/repo/issues/9\n",
                stderr="",
            )
        raise AssertionError(f"unexpected gh call: {args}")

    monkeypatch.setattr(feedback_cli.subprocess, "run", fake_run)

    result = runner.invoke(
        app,
        [
            "feedback",
            "issue",
            "create",
            exported.output.strip(),
            "--repo",
            "example/repo",
            "--confirm-create",
        ],
    )

    assert result.exit_code == 0
    assert "GitHub Issueを作成しました" in result.output
    frontmatter, _ = read_record(feedback_path)
    assert frontmatter["issue"] == {
        "provider": "github",
        "repo": "example/repo",
        "url": "https://github.com/example/repo/issues/9",
    }


def test_lab_issue_draft_sanitizes_lab_first_record(copy_fixture, monkeypatch):
    root = copy_fixture("harnessops-core-minimal")
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init", "--profile", "harnessops-core"]).exit_code == 0
    captured = runner.invoke(
        app,
        [
            "lab",
            "capture",
            "--title",
            "Lab-first issue workflow",
            "--summary",
            f"Local improvement observed at {root}/private/notes.md",
            "--expected-change",
            "Create a sanitized GitHub issue draft from the lab record.",
        ],
    )
    assert captured.exit_code == 0

    result = runner.invoke(
        app,
        [
            "lab",
            "issue",
            "draft",
            "--from",
            "FB0001",
            "--title",
            "Lab-first issue workflow",
        ],
    )

    assert result.exit_code == 0
    assert "Markdown下書きを書きました" in result.output
    assert str(root) not in result.output
    drafts = list((root / "harness-lab/views/lab-issue-drafts").glob("*github-issue-draft.md"))
    assert len(drafts) == 1
    draft = drafts[0].read_text(encoding="utf-8")
    assert "<PROJECT_ROOT>" in draft
    assert "除外した非公開情報" in draft


def test_lab_issue_create_writes_back_created_issue_url(copy_fixture, monkeypatch):
    root = copy_fixture("harnessops-core-minimal")
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init", "--profile", "harnessops-core"]).exit_code == 0
    captured = runner.invoke(
        app,
        [
            "lab",
            "capture",
            "--title",
            "Promote lab record to issue",
            "--summary",
            "Lab-first records need a GitHub issue promotion path.",
            "--expected-change",
            "Create the issue only after duplicate checks and explicit confirmation.",
        ],
    )
    assert captured.exit_code == 0

    def fake_run(args, check, capture_output, text):
        assert check is True
        assert capture_output is True
        assert text is True
        if args[:3] == ["gh", "issue", "list"]:
            return subprocess.CompletedProcess(args=args, returncode=0, stdout="[]", stderr="")
        if args[:3] == ["gh", "issue", "create"]:
            return subprocess.CompletedProcess(
                args=args,
                returncode=0,
                stdout="https://github.com/example/repo/issues/10\n",
                stderr="",
            )
        raise AssertionError(f"unexpected gh call: {args}")

    monkeypatch.setattr(feedback_cli.subprocess, "run", fake_run)

    result = runner.invoke(
        app,
        [
            "lab",
            "issue",
            "create",
            "--from",
            "FB0001",
            "--repo",
            "example/repo",
            "--confirm-create",
            "--title",
            "Promote lab record to issue",
        ],
    )

    assert result.exit_code == 0
    assert "GitHub Issueを作成しました" in result.output
    assert "Issue URLを書き戻したレコード数: 2" in result.output
    feedback_frontmatter, _ = read_record(root / "harness-lab/records/feedback/FB0001-promote-lab-record-to-issue.md")
    assert feedback_frontmatter["links"]["issue_url"] == "https://github.com/example/repo/issues/10"
    dossier_frontmatter, _ = read_record(next((root / "harness-lab/improvements").glob("IMP0001-*.md")))
    assert dossier_frontmatter["links"]["issue_url"] == "https://github.com/example/repo/issues/10"


def test_add_failure_rejects_invalid_disposition(copy_fixture, monkeypatch):
    root = copy_fixture("runops-project-minimal")
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init", "--profile", "runops-project"]).exit_code == 0

    result = runner.invoke(
        app, ["add-failure", "--title", "bad", "--disposition", "not-a-disposition"]
    )

    assert result.exit_code == 1
    assert "disposition が不正" in result.output
    assert not list((root / "harness-feedback/records/failures").glob("F*.md"))


def test_feedback_export_skips_project_evolution(copy_fixture, monkeypatch):
    root = copy_fixture("runops-project-minimal")
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init", "--profile", "runops-project"]).exit_code == 0
    assert (
        runner.invoke(
            app,
            [
                "add-failure",
                "--title",
                "research pivot only",
                "--target",
                "runops",
                "--disposition",
                "project-evolution",
            ],
        ).exit_code
        == 0
    )

    result = runner.invoke(
        app, ["feedback", "export", "--target", "runops", "--sanitize"]
    )

    assert result.exit_code == 1
    assert "一致するフィードバックレコードがありません" in result.output


def test_feedback_import_rejects_unsanitized_markdown(
    copy_fixture, tmp_path, monkeypatch
):
    root = copy_fixture("runops-upstream-minimal")
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init", "--profile", "runops-upstream"]).exit_code == 0
    bad = tmp_path / "README.md"
    bad.write_text("# Not feedback\n", encoding="utf-8")

    result = runner.invoke(app, ["feedback", "import", str(bad)])

    assert result.exit_code == 1
    assert "import には" in result.output


def test_doctor_fails_pending_migration_unless_allowed(copy_fixture, monkeypatch):
    import json

    root = copy_fixture("runops-project-minimal")
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init", "--profile", "runops-project"]).exit_code == 0
    lock = root / ".harnessops/lock.json"
    data = json.loads(lock.read_text(encoding="utf-8"))
    data["layout_version"] = "9.9"
    lock.write_text(json.dumps(data), encoding="utf-8")

    failed = runner.invoke(app, ["doctor"])
    allowed = runner.invoke(app, ["doctor", "--allow-pending"])

    assert failed.exit_code == 1
    assert "未適用マイグレーション" in failed.output
    assert allowed.exit_code == 0


def test_migrate_apply_normalizes_unsupported_layout(copy_fixture, monkeypatch):
    import json

    root = copy_fixture("runops-project-minimal")
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init", "--profile", "runops-project"]).exit_code == 0
    lock = root / ".harnessops/lock.json"
    data = json.loads(lock.read_text(encoding="utf-8"))
    data["layout_version"] = "9.9"
    lock.write_text(json.dumps(data), encoding="utf-8")

    result = runner.invoke(app, ["migrate", "--apply"])

    assert result.exit_code == 0
    assert json.loads(lock.read_text(encoding="utf-8"))["layout_version"] == "0.1"
    assert list((root / ".harnessops/migrations").glob("9.9-to-0.1.md"))


def test_adopted_decision_requires_evidence_and_guard(copy_fixture, monkeypatch):
    root = copy_fixture("runops-upstream-minimal")
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init", "--profile", "runops-upstream"]).exit_code == 0

    result = runner.invoke(app, ["decide", "--from", "H0001", "--status", "adopted"])

    assert result.exit_code == 1
    assert "adopted の判断には" in result.output


def test_sanitize_config_redacts_private_terms(copy_fixture, monkeypatch):
    root = copy_fixture("runops-project-minimal")
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init", "--profile", "runops-project"]).exit_code == 0
    sanitize_config = root / ".harnessops/sanitize.yml"
    sanitize_config.write_text("private_terms:\n  - secret-method\n", encoding="utf-8")
    assert (
        runner.invoke(
            app,
            [
                "add-failure",
                "--title",
                "Secret method leaked",
                "--target",
                "runops",
                "--context",
                "secret-method appeared in public output",
            ],
        ).exit_code
        == 0
    )

    result = runner.invoke(app, ["feedback", "export", "--sanitize"])

    assert result.exit_code == 0
    exported = root / result.output.strip()
    assert "secret-method" not in exported.read_text(encoding="utf-8")
