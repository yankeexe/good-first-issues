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
Converts the specified time range to UTC date time.

# Query all organization repos
$ gfi search "rust-lang" --period "30 hours"

# Query a specific repo in an organization
$ gfi search "rust-lang" --repo "rust" -p "30 mins"

# Query repos with the topic hacktoberfest
$ gfi search -hf -p "100 days"

# Query all user repos
$ gfi search "yankeexe" --user -p "600 hrs"

# Query a specific repo of a user
$ gfi search "yankeexe" --user --repo "good-first-issues" -p "600 days"

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
    default=10,
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
        name, repo, user, hacktoberfest, period, limit
    )

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
        issues, rate_limit = services.org_user_pipeline(response, mode)

    if mode == "search":
        issues, rate_limit = services.extract_search_results(response)
        issues = issues[:limit]  # cannot set limit on the search_query directly

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

    # Handle displaying issues on browser.
    if web:
        html_data = tabulate(issues, table_headers, tablefmt="html")
        return utils.web_server(html_data)

    row_ids = list(range(1, len(issues) + 1))
    print(
        tabulate(
            issues,
            table_headers,
            tablefmt="fancy_grid",
            showindex=row_ids,
        )
    )

    console.print(f"Remaining requests:dash:: {rate_limit}", style="bold green")
    console.print("Happy Hacking :tada::zap::rocket:", style="bold blue")
