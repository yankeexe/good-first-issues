""" GraphQL mode commands. """
from typing import List, Optional, Union, Iterable

from cliche import cli
from halo import Halo
from tabulate import tabulate
from rich.console import Console

from good_first_issues import utils
from good_first_issues.graphql import services


@cli
def gql(name: str, repo: str, limit: int = 10, all: bool = False, web: bool = False):
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
        print(f"Remaining requests:dash:: {rate_limit}")

        return print("No good first issues found!:mask:")
    # Handle limiting the output displayed.
    limiter = utils.identify_limit(limit, all)

    # Handle displaying issues on browser.
    if web:
        html_data = tabulate(issues[:limiter], table_headers, tablefmt="html")
        return utils.web_server(html_data)

    print(tabulate(issues[:limiter], table_headers, tablefmt="fancy_grid", showindex=True,))

    print(f"Remaining requests:dash:: {rate_limit}")
    print("Happy Hacking :tada::zap::rocket:")
