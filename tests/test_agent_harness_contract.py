import json
from pathlib import Path

from harnessops.core import yamlio
from harnessops.core.agent_bridge import BRIDGE_TEXT


ROOT = Path(__file__).resolve().parents[1]
MANAGED_DIRS = (".harnessops/", "harness-feedback/", "harness-lab/")


def assert_harness_contract(text: str) -> None:
    assert "hops doctor --check-overlay" in text
    for managed_dir in MANAGED_DIRS:
        assert managed_dir in text


def test_root_agent_docs_explain_hops_contract() -> None:
    for filename in ("AGENTS.md", "CLAUDE.md"):
        text = (ROOT / filename).read_text(encoding="utf-8")
        assert_harness_contract(text)
        assert "uv run --with-editable . hops <command>" in text


def test_generated_bridge_explains_hops_contract() -> None:
    assert_harness_contract(BRIDGE_TEXT)
    assert "uvx --from harnessops hops <command>" in BRIDGE_TEXT
    assert "uv run --with-editable . hops <command>" not in BRIDGE_TEXT
    assert "hops feedback export --sanitize" in BRIDGE_TEXT
    assert "hops lab capture" in BRIDGE_TEXT


def test_repo_local_bridge_expands_hops_skills(tmp_path) -> None:
    from harnessops.core.agent_bridge import write_bridge

    paths = write_bridge(tmp_path, codex=True)
    rel_paths = {path.relative_to(tmp_path).as_posix() for path in paths}
    assert ".agents/skills/harnessops-bridge/SKILL.md" in rel_paths
    assert ".agents/skills/hops-add-failure/SKILL.md" in rel_paths
    assert ".agents/skills/hops-issue-triage/SKILL.md" in rel_paths


def test_harnessops_repo_has_repo_local_hops_skills() -> None:
    for skill_name in (
        "hops-add-failure",
        "hops-compact-lab-memory",
        "hops-issue-triage",
        "hops-research-improvements",
        "hops-run-lab",
        "hops-update-harness",
    ):
        text = (ROOT / f".agents/skills/{skill_name}/SKILL.md").read_text(encoding="utf-8")
        assert_harness_contract(text)
    run_lab = (ROOT / ".agents/skills/hops-run-lab/SKILL.md").read_text(encoding="utf-8")
    assert "hops lab capture" in run_lab
    assert "hops lab investigate" in run_lab
    assert "hops lab classify" in run_lab
    assert "hops lab memory lint" in run_lab
    assert "メタ仮説スキャン" in run_lab


def test_packaged_plugin_skills_explain_hops_contract() -> None:
    skill_paths = sorted((ROOT / "plugins").glob("*/harnessops/skills/*/SKILL.md"))
    assert skill_paths
    for path in skill_paths:
        text = path.read_text(encoding="utf-8")
        assert_harness_contract(text)
        assert "uv run --with-editable . hops <command>" not in text


def test_packaged_agent_assets_match_plugin_skills() -> None:
    for host in ("codex", "claude"):
        asset_manifest = ROOT / f"src/harnessops/agent_assets/plugins/{host}/harnessops"
        assert (asset_manifest / "README.md").exists()
        assert any((asset_manifest / marker).exists() for marker in (".codex-plugin/plugin.json", ".claude-plugin/plugin.json"))
        plugin_skills = sorted((ROOT / f"plugins/{host}/harnessops/skills").glob("*/SKILL.md"))
        asset_skills = sorted((asset_manifest / "skills").glob("*/SKILL.md"))
        assert [path.parent.name for path in asset_skills] == [path.parent.name for path in plugin_skills]
        for plugin_skill, asset_skill in zip(plugin_skills, asset_skills, strict=True):
            assert asset_skill.read_text(encoding="utf-8") == plugin_skill.read_text(encoding="utf-8")


def test_packaged_plugin_readmes_explain_hops_contract() -> None:
    readme_paths = sorted((ROOT / "plugins").glob("*/harnessops/README.md"))
    assert readme_paths
    for path in readme_paths:
        text = path.read_text(encoding="utf-8")
        assert_harness_contract(text)
        assert "uvx --from harnessops hops agent install" in text
        assert "uv run --with-editable . hops agent install" not in text
    for path in readme_paths:
        assert "hops agent bridge" in path.read_text(encoding="utf-8")


def test_lifecycle_delegation_contract_is_documented() -> None:
    docs = [
        ROOT / "SPEC.md",
        ROOT / "specs/harness-common-spec.md",
        ROOT / "docs/target-integration-agent-brief.md",
        ROOT / "docs/project-repository-integration-agent-brief.md",
    ]
    for path in docs:
        text = path.read_text(encoding="utf-8")
        assert "update-harness" in text
        assert "hops doctor --check-overlay --check-records" in text
        assert "hops migrate --check" in text
        assert "hops migrate --apply" in text

    target_brief = (ROOT / "docs/target-integration-agent-brief.md").read_text(encoding="utf-8")
    assert "repo-local skill" in target_brief
    assert "global plugin" in target_brief
    assert "hops agent bridge --codex" in target_brief

    project_brief = (ROOT / "docs/project-repository-integration-agent-brief.md").read_text(encoding="utf-8")
    assert "repo-local skill" in project_brief
    assert "global plugin" in project_brief


def test_feedback_triage_ownership_contract_is_documented() -> None:
    docs = [
        ROOT / "SPEC.md",
        ROOT / "specs/feedback-routing-spec.md",
        ROOT / "docs/agent-user-guide.md",
        ROOT / "docs/target-integration-agent-brief.md",
        ROOT / "docs/project-repository-integration-agent-brief.md",
    ]
    for path in docs:
        text = path.read_text(encoding="utf-8")
        assert "domain" in text
        assert "routing" in text
        assert "sanitize" in text

    cli_spec = (ROOT / "specs/cli-spec.md").read_text(encoding="utf-8")
    assert "hops feedback add --target <target>" in cli_spec
    assert "hops add-failure" in cli_spec
    assert "hops add-feedback --from <Fid>" in cli_spec


def test_builtin_profiles_expose_domain_triage_hooks() -> None:
    profile_paths = sorted((ROOT / "src/harnessops/profiles/builtins").glob("*.yml"))
    assert profile_paths
    for path in profile_paths:
        profile = yamlio.safe_load(path.read_text(encoding="utf-8"))
        domain_triage = profile.get("domain_triage")
        assert isinstance(domain_triage, dict), path
        assert domain_triage.get("skill"), path
        assert domain_triage.get("scope"), path
        assert domain_triage.get("delegates_to_harnessops"), path


def test_release_skill_is_repo_local() -> None:
    release_skill = ROOT / ".agents/skills/release/SKILL.md"
    text = release_skill.read_text(encoding="utf-8")
    assert "repo-local skill" in text
    assert "gh release create" in text
    assert "hops lab capture" in text
    assert "hops doctor --check-overlay --check-records" in text
    assert not (ROOT / "plugins/codex/harnessops/skills/hops-release/SKILL.md").exists()
    assert not (ROOT / "plugins/claude/harnessops/skills/hops-release/SKILL.md").exists()


def test_codex_marketplace_exposes_packaged_plugin() -> None:
    marketplace = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text(encoding="utf-8"))
    entry = next(plugin for plugin in marketplace["plugins"] if plugin["name"] == "harnessops")
    assert entry["source"] == {"source": "local", "path": "./plugins/codex/harnessops"}
    assert entry["policy"]["installation"] == "AVAILABLE"
    assert (ROOT / "plugins/codex/harnessops/.codex-plugin/plugin.json").exists()


def test_issue_triage_skill_is_packaged() -> None:
    for host in ("codex", "claude"):
        skill = ROOT / f"plugins/{host}/harnessops/skills/hops-issue-triage/SKILL.md"
        text = skill.read_text(encoding="utf-8")
        assert "hops feedback import --issue" in text
        assert "hops lab new-eval-case" in text
        assert_harness_contract(text)


def test_update_harness_skill_is_packaged() -> None:
    for host in ("codex", "claude"):
        skill = ROOT / f"plugins/{host}/harnessops/skills/hops-update-harness/SKILL.md"
        text = skill.read_text(encoding="utf-8")
        assert "hops update-harness" in text
        assert ".new" in text
        assert_harness_contract(text)


def test_lab_capture_contract_is_documented() -> None:
    docs = [
        ROOT / "SPEC.md",
        ROOT / "specs/cli-spec.md",
        ROOT / "docs/agent-user-guide.md",
        ROOT / "docs/target-integration-agent-brief.md",
    ]
    for path in docs:
        assert "hops lab capture" in path.read_text(encoding="utf-8")
        assert "hops lab compact" in path.read_text(encoding="utf-8")
        assert "hops lab memory lint" in path.read_text(encoding="utf-8")
        assert "hops lab research-scan" in path.read_text(encoding="utf-8")
    for host in ("codex", "claude"):
        text = (ROOT / f"plugins/{host}/harnessops/skills/hops-run-lab/SKILL.md").read_text(encoding="utf-8")
        assert "hops lab capture" in text
        assert "hops lab investigate" in text
        assert "hops lab classify" in text
        assert "hops lab compact" in text
        assert "hops lab memory lint" in text
        assert "メタ仮説スキャン" in text
        assert_harness_contract(text)


def test_meta_improvement_research_skill_is_packaged() -> None:
    repo_skill = (ROOT / ".agents/skills/hops-research-improvements/SKILL.md").read_text(encoding="utf-8")
    assert "web" in repo_skill
    assert "rg" in repo_skill
    assert "hops lab investigate" in repo_skill
    assert "hops lab classify" in repo_skill
    assert "hops lab research-scan" in repo_skill
    assert "hops lab capture" in repo_skill
    assert "hops propose" in repo_skill
    assert "メタ仮説スキャン" in repo_skill
    assert_harness_contract(repo_skill)

    for host in ("codex", "claude"):
        skill = ROOT / f"plugins/{host}/harnessops/skills/hops-research-improvements/SKILL.md"
        text = skill.read_text(encoding="utf-8")
        assert text == repo_skill
        assert_harness_contract(text)


def test_lab_memory_compaction_skill_is_packaged() -> None:
    repo_skill = (ROOT / ".agents/skills/hops-compact-lab-memory/SKILL.md").read_text(encoding="utf-8")
    assert "hops lab memory lint" in repo_skill
    assert "hops lab memory prepare" in repo_skill
    assert "lab-memory-abstraction.yml" in repo_skill
    assert "deterministic snapshot" in repo_skill
    assert_harness_contract(repo_skill)

    for host in ("codex", "claude"):
        skill = ROOT / f"plugins/{host}/harnessops/skills/hops-compact-lab-memory/SKILL.md"
        text = skill.read_text(encoding="utf-8")
        assert text == repo_skill
        assert_harness_contract(text)
