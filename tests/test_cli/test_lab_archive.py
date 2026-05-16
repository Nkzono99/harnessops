from __future__ import annotations

import json
import subprocess
import zipfile

from typer.testing import CliRunner

from harnessops.cli.main import app


runner = CliRunner()


def run_cli(args):
    result = runner.invoke(app, args)
    assert result.exit_code == 0, result.output
    return result


def run_git(root, args):
    return subprocess.run(
        ["git", *args], cwd=root, check=True, capture_output=True, text=True
    )


def _configure_git(root) -> None:
    run_git(root, ["init"])
    run_git(root, ["config", "user.email", "test@example.com"])
    run_git(root, ["config", "user.name", "HarnessOps Test"])


def test_lab_archive_pack_captures_deleted_lab_records(copy_fixture, monkeypatch):
    root = copy_fixture("harnessops-core-minimal")
    monkeypatch.chdir(root)
    _configure_git(root)
    run_cli(["init", "--profile", "harnessops-core"])
    captured = run_cli(
        [
            "lab",
            "capture",
            "--title",
            "Old lab record can leave git history",
            "--summary",
            "A source record may need to be removed from the tracked lab after release.",
            "--expected-change",
            "Release-time archive packs preserve deleted records outside the main tree.",
            "--capability",
            "lab_forgetting",
            "--failure-class",
            "git_history_retains_archived_records",
        ]
    )
    record_path = root / captured.output.strip()
    view_path = root / "harness-lab" / "views" / "imported-feedback.md"

    run_git(root, ["add", "-A"])
    run_git(root, ["commit", "-m", "baseline lab record"])
    run_git(root, ["tag", "v0.1.0"])

    record_path.unlink()
    view_path.unlink()
    run_git(root, ["add", "-A"])
    run_git(root, ["commit", "-m", "archive old lab record"])

    planned = json.loads(
        run_cli(
            [
                "lab",
                "archive",
                "plan",
                "--since-ref",
                "v0.1.0",
                "--to-ref",
                "HEAD",
                "--json",
            ]
        ).output
    )
    assert planned["eligible_count"] == 1
    assert planned["deleted_count"] == 2
    assert (
        planned["entries"][0]["path"]
        == "harness-lab/records/feedback/FB0001-old-lab-record-can-leave-git-history.md"
    )
    assert planned["excluded"][0]["path"] == "harness-lab/views/imported-feedback.md"

    packed = json.loads(
        run_cli(
            [
                "lab",
                "archive",
                "pack",
                "--since-ref",
                "v0.1.0",
                "--to-ref",
                "HEAD",
                "--out",
                "dist",
                "--asset-name",
                "harness-lab-archive-v0.1.1.zip",
                "--json",
            ]
        ).output
    )
    archive_path = root / packed["path"]
    assert packed["status"] == "written"
    assert archive_path.exists()

    with zipfile.ZipFile(archive_path) as archive:
        names = set(archive.namelist())
        assert "manifest.json" in names
        assert "SHA256SUMS" in names
        manifest = json.loads(archive.read("manifest.json").decode("utf-8"))
        archived_path = manifest["entries"][0]["archive_path"]
        assert archived_path in names
        assert "Release-time archive packs" in archive.read(archived_path).decode(
            "utf-8"
        )

    verified = json.loads(
        run_cli(["lab", "archive", "verify", str(archive_path), "--json"]).output
    )
    assert verified["ok"] is True
    assert verified["entry_count"] == 1


def test_lab_archive_pack_skips_when_no_deleted_records(copy_fixture, monkeypatch):
    root = copy_fixture("harnessops-core-minimal")
    monkeypatch.chdir(root)
    _configure_git(root)
    run_cli(["init", "--profile", "harnessops-core"])
    run_git(root, ["add", "-A"])
    run_git(root, ["commit", "-m", "baseline"])
    run_git(root, ["tag", "v0.1.0"])

    packed = json.loads(
        run_cli(["lab", "archive", "pack", "--since-ref", "v0.1.0", "--json"]).output
    )

    assert packed["status"] == "empty"
    assert packed["path"] is None
