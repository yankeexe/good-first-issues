""" GraphQL mode commands. """
from typing import List, Optional, Union, Iterable

import click
from halo import Halo
from tabulate import tabulate
from rich.console import Console

from good_first_issues import utils
from good_first_issues.graphql import services


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
    "--user",
    "-u",
    help="Specify if it's a user repository",
    is_flag=True,
)
@click.option(
    "--web",
    help="Display issues on browser",
    is_flag=True,
)
@click.option(
    "--all",
    help="View all the issues found without limits.",
    is_flag=True,
)
@click.argument("name")
def gql(name: str, repo: str, user: bool, web: bool, limit: int, all: bool):
    """
    Sub-command for GraphQL mode.
    """
    issues: Optional[Iterable] = None
    rate_limit: int = 0

    # Check for GitHub Token.
    token: Union[str, bool] = utils.check_credential()

    # Identify the flags passed.
    query, variables, mode = services.identify_mode(name, repo, user)

    # Spinner
    spinner = Halo(text="Fetching repos...", spinner="dots")
    spinner.start()

    # API Call
    response = services.caller(token, query, variables)

    spinner.succeed("Repos fetched.")

    # Data Filtering
    if mode == "org" or mode == "user":
        issues, rate_limit = services.org_user_pipeline(response, mode)

    if mode == "repo":
        issues, rate_limit = services.extract_repo_issues(response)

    table_headers: List = ["Title", "Issue URL"]

    # No good first issues found.
    if not issues:
        console.print(
            f"Remaining requests:dash:: {rate_limit}",
            style="bold green",
        )

        return console.print(
            "No good first issues found!:mask:",
            style="bold red",
        )
    # Handle limiting the output displayed.
    limiter = utils.identify_limit(limit, all)

    # Handle displaying issues on browser.
    if web:
        html_data = tabulate(issues[:limiter], table_headers, tablefmt="html")
        return utils.web_server(html_data)

    issue_count = len(issues)
    row_ids = utils.get_row_ids(issue_count, limiter)
    print(
        tabulate(
            issues[:limiter],
            table_headers,
            tablefmt="fancy_grid",
            showindex=row_ids,
        )
    )

    console.print(
        f"Remaining requests:dash:: {rate_limit}", style="bold green"
    )
    console.print("Happy Hacking :tada::zap::rocket:", style="bold blue")
