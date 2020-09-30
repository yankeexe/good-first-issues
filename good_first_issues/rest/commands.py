""" REST API mode commands. """
from typing import Union, Optional, List

from cliche import cli
from tabulate import tabulate

from good_first_issues import utils
from good_first_issues.rest import helpers, services


@cli
def get(name: str, repo: str, limit: int = 10, all: bool = False, web: bool = False):
    """
    Sub-command for REST API mode
    """
    token: Union[str, bool] = utils.check_credential()
    limiter: Optional[int] = utils.identify_limit(limit, all)
    table_headers: List[str] = ["Title", "Issues"]

    if not repo:
        issues, rate_limit = services.owner_repos(name, token, limiter)
    else:
        issues, rate_limit = services.unit_owner_repo(name, repo, token, limiter)

    # Handle empty issues.
    if not issues:
        print(f"Remaining requests {rate_limit}",)

        return print("No good first issues found!")

    # Handle displaying issues on browser.
    if web:
        html_data = tabulate(issues, table_headers, tablefmt="html")
        return utils.web_server(html_data)

    print(tabulate(issues, table_headers, tablefmt="fancy_grid", showindex=True))

    print(f"Remaining requests {rate_limit}")
    print("Happy Hacking")
