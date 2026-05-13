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
        "hops-daily-steward",
        "hops-issue-triage",
        "hops-open-meta-scan",
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


def test_pypi_publish_workflow_uses_node24_ready_actions() -> None:
    workflow = (ROOT / ".github/workflows/publish-pypi.yml").read_text(encoding="utf-8")
    assert "uses: actions/checkout@v5" in workflow
    assert "uses: actions/setup-python@v6" in workflow
    assert "uses: actions/checkout@v4" not in workflow
    assert "uses: actions/setup-python@v5" not in workflow
    assert "environment: pypi" in workflow
    assert "id-token: write" in workflow


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
    assert "hops-open-meta-scan" in repo_skill
    assert "selection/routing lane" in repo_skill
    assert "Raw Ideas Considered" in repo_skill
    assert "anti-myopia strategy pass" in repo_skill
    assert "immediate bugfix / workflow design / evaluation methodology / cross-project harness principle" in repo_skill
    assert "`local-only` / `repeated-pattern` / `cross-project` / `strategic`" in repo_skill
    assert "systemic candidate" in repo_skill
    assert "Candidate Horizon" in repo_skill
    assert "reject as local" in repo_skill
    assert "少なくとも2つの target/project repo" in repo_skill
    assert "candidate selection needs a horizon/generalization guard" in repo_skill
    assert "target/project repository" in repo_skill
    assert "harness-feedback" in repo_skill
    assert "harness-lab" in repo_skill
    assert "hops lab investigate" in repo_skill
    assert "hops lab classify" in repo_skill
    assert "hops lab research-scan" in repo_skill
    assert "hops lab capture" in repo_skill
    assert "hops propose" in repo_skill
    assert "hops add-failure" in repo_skill
    assert "hops feedback export --target <target> --sanitize" in repo_skill
    assert "project repo で `harness-lab/` を作らない" in repo_skill
    assert "メタ仮説スキャン" in repo_skill
    assert_harness_contract(repo_skill)

    for host in ("codex", "claude"):
        skill = ROOT / f"plugins/{host}/harnessops/skills/hops-research-improvements/SKILL.md"
        text = skill.read_text(encoding="utf-8")
        assert text == repo_skill
        assert_harness_contract(text)


def test_open_meta_scan_skill_is_packaged() -> None:
    repo_skill = (ROOT / ".agents/skills/hops-open-meta-scan/SKILL.md").read_text(encoding="utf-8")
    assert "open scan" in repo_skill
    assert "invention lane" in repo_skill
    assert "Raw Ideas" in repo_skill
    assert "Counterframes" in repo_skill
    assert "Do Not Record Yet" in repo_skill
    assert "hops-research-improvements" in repo_skill
    assert "デフォルトでは `hops lab capture`" in repo_skill
    assert "発想を recordable にしすぎない" in repo_skill
    assert_harness_contract(repo_skill)

    for host in ("codex", "claude"):
        skill = ROOT / f"plugins/{host}/harnessops/skills/hops-open-meta-scan/SKILL.md"
        text = skill.read_text(encoding="utf-8")
        asset = ROOT / f"src/harnessops/agent_assets/plugins/{host}/harnessops/skills/hops-open-meta-scan/SKILL.md"
        assert text == repo_skill
        assert asset.read_text(encoding="utf-8") == repo_skill
        assert_harness_contract(text)


def test_daily_steward_skill_is_packaged() -> None:
    repo_skill = (ROOT / ".agents/skills/hops-daily-steward/SKILL.md").read_text(encoding="utf-8")
    assert "steward / conductor" in repo_skill
    assert "compact steward / conductor" in repo_skill
    assert "Default automation mode is `advance-local`" in repo_skill
    assert "Human review is not required for local advance" in repo_skill
    assert "Repo Role Routing" in repo_skill
    assert "project repo | Use `harness-feedback/`" in repo_skill
    assert "Do not assume this is the HarnessOps implementation repository" in repo_skill
    assert "Non-Negotiable Gates" in repo_skill
    assert "Sync Gate" in repo_skill
    assert "hops steward preflight --pull --json" in repo_skill
    assert "git fetch --prune" in repo_skill
    assert "git pull --ff-only" in repo_skill
    assert "stash, reset, rebase, force pull" in repo_skill
    assert "automation prompt" in repo_skill
    assert "open divergent invention lane" in repo_skill
    assert "Selection Rules" in repo_skill
    assert "Advance-Local" in repo_skill
    assert "End-Of-Run Policy" in repo_skill
    assert "patch-only" in repo_skill
    assert "commit-local" in repo_skill
    assert "hops steward finalize --policy commit-local --validation-passed --json" in repo_skill
    assert "Decision Card" in repo_skill
    assert "no-op are valid outcomes" in repo_skill
    assert "hops-open-meta-scan" in repo_skill
    assert "hops-research-improvements" in repo_skill
    assert "hops-run-lab" in repo_skill
    assert "Remote actions follow explicit automation prompt authorization" in repo_skill
    assert_harness_contract(repo_skill)

    for host in ("codex", "claude"):
        skill = ROOT / f"plugins/{host}/harnessops/skills/hops-daily-steward/SKILL.md"
        text = skill.read_text(encoding="utf-8")
        asset = ROOT / f"src/harnessops/agent_assets/plugins/{host}/harnessops/skills/hops-daily-steward/SKILL.md"
        assert text == repo_skill
        assert asset.read_text(encoding="utf-8") == repo_skill
        assert_harness_contract(text)


def test_daily_steward_automation_prompt_is_documented() -> None:
    prompt_doc = (ROOT / "docs/daily-steward-automation.md").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    agent_guide = (ROOT / "docs/agent-user-guide.md").read_text(encoding="utf-8")

    assert "このリポジトリで repo-local skill `.agents/skills/hops-daily-steward/SKILL.md` を実行してください。" in prompt_doc
    assert "HarnessOps を導入した target repository / project repository にも配布して使えます" in prompt_doc
    assert "base-branch: main" in prompt_doc
    assert "project repo に `harness-lab/` を作らないでください" in prompt_doc
    assert "subagents: explicitly allowed" in prompt_doc
    assert "remote-write: automation-branch-only" in prompt_doc
    assert "base-branch-push: false" in prompt_doc
    assert "hops steward preflight --pull --json" in prompt_doc
    assert "hops steward finalize --policy commit-local --validation-passed" in prompt_doc
    assert "uv run --with-editable . hops steward" not in prompt_doc
    assert "uv run --with-editable . hops doctor" not in prompt_doc
    assert "uv run --with-editable . hops migrate" not in prompt_doc
    assert "uv run pytest" not in prompt_doc
    assert "uv run ruff" not in prompt_doc
    assert "<repo-native test command>" in prompt_doc
    assert "git push -u origin HEAD" in prompt_doc
    assert "PR、コメント、Issue、release、既定 branch push は作成しないでください。" in prompt_doc
    assert "完全自動化プロンプト: 既定 branch push と remote action" in prompt_doc
    assert "remote-write: full" in prompt_doc
    assert "base-branch-push: true" in prompt_doc
    assert "create-pr: true" in prompt_doc
    assert "issue-comment-close-create: true" in prompt_doc
    assert "release: true" in prompt_doc
    assert "hops steward finalize --policy commit-local --validation-passed --branch <base-branch>" in prompt_doc
    assert "git push origin <base-branch>" in prompt_doc
    assert "Issue の作成/コメント/クローズ、PR の作成/更新/merge、既定 branch push、release は、選択した候補の自然な次の一手であれば実行してよいです。" in prompt_doc
    assert "repo-local の `release` skill または対象リポジトリの documented release command" in prompt_doc
    assert "daily-steward-automation.md" in readme
    assert "daily-steward-automation.md" in agent_guide


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
