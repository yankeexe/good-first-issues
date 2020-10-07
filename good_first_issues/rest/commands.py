""" REST API mode commands. """
from typing import Union, Optional, List

import click
from tabulate import tabulate
from rich.console import Console

from good_first_issues import utils
from good_first_issues.rest import helpers, services


console = Console(color_system="auto")


@click.command()
@click.option(
    "--repo",
    help="Search in a specific repo of user or organization",
    type=str,
)
@click.option(
    "--limit",
    help="Limit the number of issues to display. Defaults to 10",
    type=int,
)
@click.option(
    "--web",
    help="Display issues on browser",
    is_flag=True,
)
@click.option(
    "--all",
    help="View all the issues found without limits",
    is_flag=True,
)
@click.argument("name")
def get(name: str, repo: str, limit: int, all: bool, web: bool):
    """
    Sub-command for REST API mode
    """
    token: Union[str, bool] = utils.check_credential()
    limiter: Optional[int] = utils.identify_limit(limit, all)
    table_headers: List[str] = ["Title", "Issues"]

    if not repo:
        issues, rate_limit = services.owner_repos(name, token, limiter)
    else:
        issues, rate_limit = services.unit_owner_repo(
            name, repo, token, limiter
        )

    # Handle empty issues.
    if not issues:
        console.print(
            f"Remaining requests:dash:: {rate_limit}",
            style="bold green",
        )

        return console.print(
            "No good first issues found!:mask:",
            style="bold red",
        )

    # Handle displaying issues on browser.
    if web:
        html_data = tabulate(issues, table_headers, tablefmt="html")
        return utils.web_server(html_data)

    issue_count: int = len(issues)
    row_ids: List[int] = utils.get_row_ids(issue_count, limiter)
    print(
        tabulate(
            issues,
            table_headers,
            tablefmt="fancy_grid",
            showindex=row_ids,
        )
    )

    console.print(
        f"Remaining requests:dash:: {rate_limit}", style="bold green"
    )
    console.print("Happy Hacking :tada::zap::rocket:", style="bold blue")
