import sys
from typing import Iterable, List, Optional, Union

import click
from halo import Halo
from rich.console import Console
from tabulate import tabulate

from good_first_issues import utils
from good_first_issues.graphql import services
from good_first_issues.utils import ParsedDuration, parse_period

console = Console(color_system="auto")


period_help_msg = """
Specify a time range for filtering data.

Converts the specified time range to UTC date time

--period 1 m,min,mins,minutes

--period 2 h,hr,hour,hours,hrs

--period 3 d,day,days

"""


@click.command()
@click.option(
    "--repo",
    "-r",
    help="Search in a specific repo of user or organization",
    type=str,
)
@click.option(
    "--hacktoberfest",
    "-hf",
    help="Search repositories with topic hacktoberfest",
    is_flag=True,
)
@click.option(
    "--limit",
    "-l",
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
    "-a",
    help="View all the issues found without limits.",
    is_flag=True,
)
@click.option("--period", "-p", help=period_help_msg)
@click.argument("name", required=False)
def search(
    name: str,
    repo: str,
    user: bool,
    web: bool,
    limit: int,
    all: bool,
    hacktoberfest: bool,
    period: str,
):
    """Search for good first issues in organizations or user repositories.

    Usage:

    gfi search <repo-owner/org-name>

    ➡️ repo owner

        gfi search "yankeexe" --user

    ➡️ org name

        gfi search "ollama"

    ➡️ search in a particular repo

        gfi search "yankeexe" --repo "good-first-issues"

        gfi search "ollama" --repo "ollama-python"

    """

    if name is None and hacktoberfest is False:
        utils.print_help_msg(search)
        sys.exit()

    issues: Optional[Iterable] = None
    rate_limit: int = 0

    # Check for GitHub Token.
    token: Union[str, bool] = utils.check_credential()

    if period:
        period: ParsedDuration = parse_period(period)
        period = period.utc_date_time.strftime("%Y-%m-%dT%H:%M:%SZ")

    # Identify the flags passed.
    query, variables, mode = services.identify_mode(
        name, repo, user, hacktoberfest, period
    )

    # Spinner
    spinner = Halo(text="Fetching repos...", spinner="dots")
    # spinner.start()

    # API Call
    response = services.caller(token, query, variables)
    breakpoint()

    spinner.succeed("Repos fetched.")

    # Data Filtering
    if mode == "org" or mode == "user":
        issues, rate_limit = services.org_user_pipeline(response, mode)

    if mode == "repo":
        issues, rate_limit = services.extract_repo_issues(response)

    if mode == "search":
        issues, rate_limit = services.extract_search_results(response)

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

    issue_count: int = len(issues)
    row_ids: List[int] = utils.get_row_ids(issue_count, limiter)
    print(
        tabulate(
            issues[:limiter],
            table_headers,
            tablefmt="fancy_grid",
            showindex=row_ids,
        )
    )

    console.print(f"Remaining requests:dash:: {rate_limit}", style="bold green")
    console.print("Happy Hacking :tada::zap::rocket:", style="bold blue")
