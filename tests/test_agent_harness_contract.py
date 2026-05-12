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
    assert "uv run --with-editable . hops <command>" in BRIDGE_TEXT
    assert "hops feedback export --sanitize" in BRIDGE_TEXT


def test_packaged_plugin_skills_explain_hops_contract() -> None:
    skill_paths = sorted((ROOT / "plugins").glob("*/harnessops/skills/*/SKILL.md"))
    assert skill_paths
    for path in skill_paths:
        assert_harness_contract(path.read_text(encoding="utf-8"))


def test_packaged_plugin_readmes_explain_hops_contract() -> None:
    readme_paths = sorted((ROOT / "plugins").glob("*/harnessops/README.md"))
    assert readme_paths
    for path in readme_paths:
        text = path.read_text(encoding="utf-8")
        assert_harness_contract(text)
        assert "hops agent bridge" in text


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
    assert "hops agent install --codex --scope user" in target_brief
    assert "hops agent bridge --codex" in target_brief


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
