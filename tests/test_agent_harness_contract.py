from pathlib import Path

from harnessops.core import yamlio
from harnessops.core.agent_bridge import BRIDGE_TEXT, bridge_text_for_mode


ROOT = Path(__file__).resolve().parents[1]
MANAGED_DIRS = (".harnessops/", "harness-feedback/", "harness-lab/")


def packaged_skill(host: str, name: str) -> Path:
    return ROOT / f"src/harnessops/agent_assets/skills/{host}/harnessops/skills/{name}/SKILL.md"


def assert_harness_contract(text: str) -> None:
    assert "hops doctor --check-overlay" in text
    for managed_dir in MANAGED_DIRS:
        assert managed_dir in text


def test_root_agent_docs_explain_hops_contract() -> None:
    for filename in ("AGENTS.md", "CLAUDE.md"):
        text = (ROOT / filename).read_text(encoding="utf-8")
        assert_harness_contract(text)
        assert "uvx --from harnessops hops <command>" in text
        assert "uv run --with-editable . hops <command>" not in text
    assert "GitHub Flow" in (ROOT / "AGENTS.md").read_text(encoding="utf-8")


def test_generated_bridge_explains_hops_contract() -> None:
    assert_harness_contract(BRIDGE_TEXT)
    assert "uvx --from harnessops hops <command>" in BRIDGE_TEXT
    assert "uv run --with-editable . hops <command>" not in BRIDGE_TEXT
    assert "hops feedback import <bundle-path>" in BRIDGE_TEXT
    assert "hops lab capture" in BRIDGE_TEXT


def test_generated_bridge_scopes_feedback_source_interface() -> None:
    text = bridge_text_for_mode("feedback-source")
    assert_harness_contract(text)
    assert "feedback-source interface" in text
    assert "hops feedback export --sanitize" in text
    assert "hops add-failure" in text
    assert "uvx --from harnessops hops lab capture" not in text
    assert "uvx --from harnessops hops propose" not in text
    assert "uvx --from harnessops hops decide" not in text


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


def test_packaged_skill_assets_explain_hops_contract() -> None:
    skill_paths = sorted((ROOT / "src/harnessops/agent_assets/skills").glob("*/harnessops/skills/*/SKILL.md"))
    assert skill_paths
    for path in skill_paths:
        text = path.read_text(encoding="utf-8")
        assert_harness_contract(text)
        assert "uvx --from harnessops hops <command>" in text
        assert "uv run --with-editable . hops <command>" not in text


def test_packaged_agent_assets_match_repo_local_skills() -> None:
    for host in ("codex", "claude"):
        asset_manifest = ROOT / f"src/harnessops/agent_assets/skills/{host}/harnessops"
        asset_skills = sorted((asset_manifest / "skills").glob("*/SKILL.md"))
        assert [path.parent.name for path in asset_skills] == [
            path.parent.name for path in sorted((ROOT / ".agents/skills").glob("hops-*/SKILL.md"))
        ]
        for asset_skill in asset_skills:
            assert_harness_contract(asset_skill.read_text(encoding="utf-8"))

    repo_skills = sorted((ROOT / ".agents/skills").glob("hops-*/SKILL.md"))
    codex_skills = sorted((ROOT / "src/harnessops/agent_assets/skills/codex/harnessops/skills").glob("*/SKILL.md"))
    for repo_skill, asset_skill in zip(repo_skills, codex_skills, strict=True):
        assert asset_skill.read_text(encoding="utf-8") == repo_skill.read_text(encoding="utf-8")


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
    assert "global plugin" not in target_brief
    assert "hops agent bridge --codex" in target_brief

    project_brief = (ROOT / "docs/project-repository-integration-agent-brief.md").read_text(encoding="utf-8")
    assert "repo-local skill" in project_brief
    assert "global plugin" not in project_brief


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
    assert not packaged_skill("codex", "hops-release").exists()
    assert not packaged_skill("claude", "hops-release").exists()


def test_pypi_publish_workflow_uses_node24_ready_actions() -> None:
    workflow = (ROOT / ".github/workflows/publish-pypi.yml").read_text(encoding="utf-8")
    assert "uses: actions/checkout@v5" in workflow
    assert "uses: actions/setup-python@v6" in workflow
    assert "uses: actions/checkout@v4" not in workflow
    assert "uses: actions/setup-python@v5" not in workflow
    assert "environment: pypi" in workflow
    assert "id-token: write" in workflow


def test_root_plugin_surface_is_removed() -> None:
    assert not (ROOT / "plugins").exists()
    assert not (ROOT / ".agents/plugins/marketplace.json").exists()


def test_issue_triage_skill_is_packaged() -> None:
    repo_skill = (ROOT / ".agents/skills/hops-issue-triage/SKILL.md").read_text(encoding="utf-8")
    assert "引数なしの open issue triage" in repo_skill
    assert "gh issue list --repo <owner/repo> --state open" in repo_skill
    assert "対応推奨 (高)" in repo_skill
    assert "対応推奨 (中)" in repo_skill
    assert "保留 / 要議論" in repo_skill
    assert "close 推奨" in repo_skill
    assert "spam、malicious、unrelated" in repo_skill
    assert "Closes #N" in repo_skill
    assert "remote_action_allowed" in repo_skill
    assert_harness_contract(repo_skill)

    for host in ("codex", "claude"):
        skill = packaged_skill(host, "hops-issue-triage")
        text = skill.read_text(encoding="utf-8")
        assert text == repo_skill
        assert "hops feedback import --issue" in text
        assert "hops lab new-eval-case" in text
        assert_harness_contract(text)


def test_update_harness_skill_is_packaged() -> None:
    for host in ("codex", "claude"):
        skill = packaged_skill(host, "hops-update-harness")
        text = skill.read_text(encoding="utf-8")
        assert "hops update-harness" in text
        assert "uvx --refresh-package harnessops --from harnessops hops update-harness --agent-bridge" in text
        assert "uvx --refresh-package harnessops --from harnessops hops update-harness --plan-upgrade" in text
        assert "uvx --refresh-package harnessops --from harnessops hops update-harness --apply-upgrade-chain" in text
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
        text = packaged_skill(host, "hops-run-lab").read_text(encoding="utf-8")
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
    assert "Candidate Queue" in repo_skill
    assert "selected_for_execution" in repo_skill
    assert "queued_for_later" in repo_skill
    assert "record_only" in repo_skill
    assert "単一候補へ潰さない" in repo_skill
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
        skill = packaged_skill(host, "hops-research-improvements")
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
        skill = packaged_skill(host, "hops-open-meta-scan")
        text = skill.read_text(encoding="utf-8")
        assert text == repo_skill
        assert_harness_contract(text)


def test_daily_steward_skill_is_packaged() -> None:
    repo_skill = (ROOT / ".agents/skills/hops-daily-steward/SKILL.md").read_text(encoding="utf-8")
    assert "steward / conductor" in repo_skill
    assert "must not stop at status reporting" in repo_skill
    assert "proactive discovery" in repo_skill
    assert "Role Routing" in repo_skill
    assert "Project repo: use `harness-feedback/`" in repo_skill
    assert "Global Gates" in repo_skill
    assert "Gate Levels" in repo_skill
    assert "hops steward preflight --pull --json" in repo_skill
    assert "Update Lane" in repo_skill
    assert "Do not start every daily run by updating HarnessOps to the latest release" in repo_skill
    assert "uvx --refresh-package harnessops --from harnessops hops update-harness" in repo_skill
    assert "Record gate" in repo_skill
    assert "Implementation gate" in repo_skill
    assert "Merge gate" in repo_skill
    assert "stash, reset, rebase, force-push" in repo_skill
    assert "automation prompt" in repo_skill
    assert "Work Budgets" in repo_skill
    assert "discovery cards: 8" in repo_skill
    assert "Candidate count is not the primary limit" in repo_skill
    assert "No-Idle Policy" in repo_skill
    assert "No-op is valid only" in repo_skill
    assert "status-only no-op" in repo_skill
    assert "no-argument open issue discovery" in repo_skill
    assert "hops-open-meta-scan" in repo_skill
    assert "hops-research-improvements" in repo_skill
    assert "hops-run-lab" in repo_skill
    assert "Remote actions follow explicit automation prompt authorization" in repo_skill
    assert "max-systemic-candidates" not in repo_skill
    assert "systemic candidate: max 1" not in repo_skill
    assert_harness_contract(repo_skill)

    for host in ("codex", "claude"):
        skill = packaged_skill(host, "hops-daily-steward")
        text = skill.read_text(encoding="utf-8")
        assert text == repo_skill
        assert_harness_contract(text)


def test_daily_steward_automation_prompt_is_documented() -> None:
    prompt_doc = (ROOT / "docs/daily-steward-automation.md").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    agent_guide = (ROOT / "docs/agent-user-guide.md").read_text(encoding="utf-8")

    assert "このリポジトリで repo-local skill `.agents/skills/hops-daily-steward/SKILL.md` を実行してください。" in prompt_doc
    assert "HarnessOps を導入した target repository / project repository にも配布して使えます" in prompt_doc
    assert "強い自動化" in prompt_doc
    assert "status-only no-op を通常結果にせず" in prompt_doc
    assert "base-branch: main" in prompt_doc
    assert "project repo に `harness-lab/` を作らないでください" in prompt_doc
    assert "subagents: explicitly allowed" in prompt_doc
    assert "merge-target-branch: main" in prompt_doc
    assert "Budgets:" in prompt_doc
    assert "discovery-cards: 8" in prompt_doc
    assert "recordable-candidates: 5" in prompt_doc
    assert "low-risk-work-packets: 5" in prompt_doc
    assert "medium-risk-work-packets: 3" in prompt_doc
    assert "high-risk-work-packets: 1" in prompt_doc
    assert "remote-write: automation-branch-merge" in prompt_doc
    assert "protected-branch-direct-push: false" in prompt_doc
    assert "create/update/merge automation PRs: true" in prompt_doc
    assert "create/comment/close GitHub issues: true" in prompt_doc
    assert "release: true, only when repo-native release criteria are met" in prompt_doc
    assert "Update lane:" in prompt_doc
    assert "do not update HarnessOps to latest as a mandatory start step" in prompt_doc
    assert "uvx --refresh-package harnessops --from harnessops hops update-harness" in prompt_doc
    assert "hops steward preflight --pull --json" in prompt_doc
    assert "hops steward finalize --policy commit-local --validation-passed" in prompt_doc
    assert "uv run --with-editable . hops steward" not in prompt_doc
    assert "uv run --with-editable . hops doctor" not in prompt_doc
    assert "uv run --with-editable . hops migrate" not in prompt_doc
    assert "uv run pytest" not in prompt_doc
    assert "uv run ruff" not in prompt_doc
    assert "repo-native test/lint/build/domain checks" in prompt_doc
    assert "git push -u origin HEAD" in prompt_doc
    assert "max-systemic-candidates" not in prompt_doc
    assert "release: false" not in prompt_doc
    assert "推奨プロンプト" not in prompt_doc
    assert "## Prompt" in prompt_doc
    assert "hops-open-meta-scan" in prompt_doc
    assert "hops-research-improvements" in prompt_doc
    assert 'hops steward finalize --policy commit-local --validation-passed --branch "codex/steward/<YYYYMMDD>-daily"' in prompt_doc
    assert "documented release command or repo-local release skill" in prompt_doc
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
        skill = packaged_skill(host, "hops-compact-lab-memory")
        text = skill.read_text(encoding="utf-8")
        assert text == repo_skill
        assert_harness_contract(text)
