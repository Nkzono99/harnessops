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
    assert "hops feedback add-failure" in text
    assert "uvx --from harnessops hops lab capture" not in text
    assert "uvx --from harnessops hops lab propose" not in text
    assert "uvx --from harnessops hops lab decide" not in text


def test_repo_local_bridge_expands_hops_skills(tmp_path) -> None:
    from harnessops.core.agent_bridge import write_bridge

    paths = write_bridge(tmp_path, codex=True)
    rel_paths = {path.relative_to(tmp_path).as_posix() for path in paths}
    assert ".agents/skills/harnessops-bridge/SKILL.md" in rel_paths
    assert ".agents/skills/hops-add-failure/SKILL.md" in rel_paths
    assert ".agents/skills/hops-github-flow/SKILL.md" in rel_paths
    assert ".agents/skills/hops-issue-triage/SKILL.md" in rel_paths


def test_harnessops_repo_has_repo_local_hops_skills() -> None:
    for skill_name in (
        "hops-add-failure",
        "hops-compact-lab-memory",
        "hops-daily-steward",
        "hops-finalize-steward",
        "hops-github-flow",
        "hops-invention-steward",
        "hops-issue-triage",
        "hops-issue-execution-steward",
        "hops-maintenance-steward",
        "hops-open-meta-scan",
        "hops-priority-improvement-steward",
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
    assert "AGENTS.md / CLAUDE.md への短い導線" in target_brief
    assert "project repo に配る案内では、feedback / lifecycle に閉じ" in target_brief

    project_brief = (ROOT / "docs/project-repository-integration-agent-brief.md").read_text(encoding="utf-8")
    assert "repo-local skill" in project_brief
    assert "global plugin" not in project_brief
    assert "HarnessOps は `harness-feedback/` でハーネス摩擦" in project_brief
    assert "`harness-lab/`、採用判断、GitHub Flow は target/meta repo 側" in project_brief


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
    assert "hops feedback add-failure" in cli_spec
    assert "hops feedback route" in cli_spec
    assert "hops feedback add --from <Fid>" in cli_spec


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


def test_pr_ci_workflow_provides_required_check_context() -> None:
    workflow = (ROOT / ".github/workflows/pr-ci.yml").read_text(encoding="utf-8")
    assert "name: PR CI" in workflow
    assert "pull_request:" in workflow
    assert "branches: [main]" in workflow
    assert "uses: actions/checkout@v5" in workflow
    assert "uses: actions/setup-python@v6" in workflow
    assert "name: pr-ci" in workflow
    assert "uv run ruff check src tests" in workflow
    assert "uv run pytest" in workflow
    assert "uv run --with-editable . hops doctor --check-overlay --check-records" in workflow
    assert "uv run --with-editable . hops migrate --check" in workflow


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
        assert "hops lab eval-case create" in text
        assert_harness_contract(text)


def test_update_harness_skill_is_packaged() -> None:
    repo_skill = (ROOT / ".agents/skills/hops-update-harness/SKILL.md").read_text(encoding="utf-8")
    assert "AGENTS.md" in repo_skill
    assert "CLAUDE.md" in repo_skill
    assert "HarnessOps 導線だけを短く確認" in repo_skill
    assert "uv run --with-editable . hops ..." in repo_skill
    assert "project repo は feedback / lifecycle に閉じ" in repo_skill
    assert "GitHub Flow は target/meta repo 側" in repo_skill
    for host in ("codex", "claude"):
        skill = packaged_skill(host, "hops-update-harness")
        text = skill.read_text(encoding="utf-8")
        assert text == repo_skill
        assert "hops update-harness" in text
        assert "uvx --refresh-package harnessops --from harnessops hops update-harness --agent-bridge" in text
        assert "uvx --refresh-package harnessops --from harnessops hops update-harness --plan-upgrade" in text
        assert "uvx --refresh-package harnessops --from harnessops hops update-harness --apply-upgrade-chain" in text
        assert ".new" in text
        assert_harness_contract(text)


def test_github_flow_skill_is_packaged() -> None:
    repo_skill = (ROOT / ".agents/skills/hops-github-flow/SKILL.md").read_text(encoding="utf-8")
    assert "hops github-flow preflight" in repo_skill
    assert "hops github-flow publish" in repo_skill
    assert "hops github-flow pr" in repo_skill
    assert "hops github-flow merge" in repo_skill
    assert "project repo" in repo_skill
    assert "--no-github-flow" in repo_skill
    assert_harness_contract(repo_skill)

    for host in ("codex", "claude"):
        text = packaged_skill(host, "hops-github-flow").read_text(encoding="utf-8")
        assert text == repo_skill
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
        assert "hops lab memory compact" in path.read_text(encoding="utf-8")
        assert "hops lab memory lint" in path.read_text(encoding="utf-8")
        assert "hops lab research-scan" in path.read_text(encoding="utf-8")
    for host in ("codex", "claude"):
        text = packaged_skill(host, "hops-run-lab").read_text(encoding="utf-8")
        assert "hops lab capture" in text
        assert "hops lab investigate" in text
        assert "hops lab classify" in text
        assert "hops lab memory compact" in text
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
    assert "hops lab propose" in repo_skill
    assert "hops feedback add-failure" in repo_skill
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
    assert "thin supervisor" in repo_skill
    assert "must not perform maintenance" in repo_skill
    assert "supervisor_plan" in repo_skill
    assert "Do not read each lane skill body up front" in repo_skill
    assert "hops steward run start --pull --json" in repo_skill
    assert "--update-policy apply" in repo_skill
    assert "hops steward run record-lane-result" in repo_skill
    assert "hops steward run end" in repo_skill
    assert "inline_fallback=true" in repo_skill
    assert "stash, reset, rebase, force-push" in repo_skill
    assert "automation prompt" in repo_skill
    assert "max-systemic-candidates" not in repo_skill
    assert "systemic candidate: max 1" not in repo_skill
    assert_harness_contract(repo_skill)

    for host in ("codex", "claude"):
        skill = packaged_skill(host, "hops-daily-steward")
        text = skill.read_text(encoding="utf-8")
        assert text == repo_skill
        assert_harness_contract(text)


def test_daily_lane_steward_skills_are_packaged() -> None:
    required = {
        "hops-maintenance-steward": [
            "hops-update-harness",
            "update-policy: apply",
            "hops-compact-lab-memory",
        ],
        "hops-issue-execution-steward": [
            "hops-issue-triage",
            "remote_action_allowed",
            "hops feedback export",
        ],
        "hops-invention-steward": [
            "hops-open-meta-scan",
            "hops-research-improvements",
            "parked/rejected ideas",
        ],
        "hops-priority-improvement-steward": [
            "T2/T3",
            "hops-run-lab",
            "guard",
        ],
        "hops-finalize-steward": [
            "hops github-flow publish",
            "hops github-flow merge --require-checks",
            "Release only when",
        ],
    }
    for skill_name, snippets in required.items():
        repo_skill = (ROOT / f".agents/skills/{skill_name}/SKILL.md").read_text(encoding="utf-8")
        assert_harness_contract(repo_skill)
        for snippet in snippets:
            assert snippet in repo_skill
        for host in ("codex", "claude"):
            text = packaged_skill(host, skill_name).read_text(encoding="utf-8")
            assert text == repo_skill
            assert_harness_contract(text)


def test_daily_steward_automation_prompt_is_documented() -> None:
    prompt_doc = (ROOT / "docs/daily-steward-automation.md").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    agent_guide = (ROOT / "docs/agent-user-guide.md").read_text(encoding="utf-8")

    assert "このリポジトリで repo-local skill `.agents/skills/hops-daily-steward/SKILL.md` を実行してください。" in prompt_doc
    assert "HarnessOps を導入した target repository / project repository にも配布して使えます" in prompt_doc
    assert "強い自動化" in prompt_doc
    assert "prompt を太らせず" in prompt_doc
    assert "base-branch: main" in prompt_doc
    assert "project repo に `harness-lab/` を作らないでください" in prompt_doc
    assert "subagents: explicitly allowed" in prompt_doc
    assert "merge-target-branch: main" in prompt_doc
    assert "remote-write: automation-branch-merge" in prompt_doc
    assert "update-policy: apply" in prompt_doc
    assert "protected-branch-direct-push: false" in prompt_doc
    assert "create/update/merge automation PRs: true" in prompt_doc
    assert "create/comment/close GitHub issues: true" in prompt_doc
    assert "release: true, only when repo-native release criteria are met" in prompt_doc
    assert "do not perform lane work directly" in prompt_doc
    assert "hops steward run start --pull --json --update-policy apply" in prompt_doc
    assert "hops steward run record-lane-result" in prompt_doc
    assert "hops steward run end" in prompt_doc
    assert "supervisor_plan" in prompt_doc
    assert "hops github-flow publish" in prompt_doc
    assert "hops github-flow pr" in prompt_doc
    assert "hops github-flow merge --require-checks" in prompt_doc
    assert "uv run --with-editable . hops steward" not in prompt_doc
    assert "uv run --with-editable . hops doctor" not in prompt_doc
    assert "uv run --with-editable . hops migrate" not in prompt_doc
    assert "uv run pytest" not in prompt_doc
    assert "uv run ruff" not in prompt_doc
    assert "repo-native validation" in prompt_doc
    assert "git push -u origin HEAD" not in prompt_doc
    assert "max-systemic-candidates" not in prompt_doc
    assert "release: false" not in prompt_doc
    assert "推奨プロンプト" not in prompt_doc
    assert "## Prompt" in prompt_doc
    assert 'hops github-flow publish --branch "codex/steward/<YYYYMMDD>-daily"' in prompt_doc
    assert "release skill or documented command" in prompt_doc
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
