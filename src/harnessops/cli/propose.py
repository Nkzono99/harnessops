from __future__ import annotations

import typer

from harnessops.cli.deprecation import warn_if_deprecated
from harnessops.core.paths import find_root
from harnessops.core.project import load_project
from harnessops.core.lab_records import create_hypothesis
from harnessops.core.record_index import find_record
from harnessops.core.record_io import read_record


def propose_command(
    from_id: str = typer.Option(..., "--from"),
    manual_template: bool = typer.Option(True, "--manual-template/--agent-assisted"),
    hypothesis: str = typer.Option("", "--hypothesis"),
    mechanism: str = typer.Option("", "--mechanism"),
    minimal_implementation: str = typer.Option("", "--minimal-implementation"),
    alternative: str = typer.Option("", "--alternative"),
    expected_upside: str = typer.Option("", "--expected-upside"),
    expected_downside: str = typer.Option("", "--expected-downside"),
    evaluation_plan: str = typer.Option("", "--evaluation-plan"),
    kill_criteria: str = typer.Option("", "--kill-criteria"),
) -> None:
    """評価ケースから改善仮説を作成します。"""
    warn_if_deprecated("propose", "hops lab propose")
    if not manual_template:
        typer.echo("エージェント支援生成は利用できません。証拠テンプレートを書き込みます")
    root = find_root()
    project = load_project(root)
    eval_path = find_record(project, from_id)
    frontmatter, _ = read_record(eval_path)
    path = create_hypothesis(
        project,
        eval_case_id=str(frontmatter.get("id", from_id)),
        title=f"{eval_path.stem} の仮説",
        capability=str(frontmatter.get("capability", "unclassified")),
        hypothesis=hypothesis,
        mechanism=mechanism,
        minimal_implementation=minimal_implementation,
        alternative=alternative,
        expected_upside=expected_upside,
        expected_downside=expected_downside,
        evaluation_plan=evaluation_plan,
        kill_criteria=kill_criteria,
    )
    typer.echo(path.relative_to(root).as_posix())


def register(app: typer.Typer) -> None:
    app.command("propose", hidden=True)(propose_command)
