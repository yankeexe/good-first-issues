""" Services for REST API mode. """
import sys
import concurrent.futures
from typing import Dict, List, Tuple, Union, Optional

import requests
from halo import Halo
from rich.console import Console
from requests.models import Response

from gfi.rest import helpers


# Initializations
# spinner variable for caller method's except blocks.
spinner = Halo(text="Fetching repos...", spinner="dots")
console = Console(color_system="auto")

# Global Variables
request_headers: Dict = dict()

# Type Aliases
UnitOwnerRepo = Tuple[Union[List, bool], Optional[str]]
OwnerRepos = Tuple[Union[List[str], bool], Optional[str]]


def unit_owner_repo(name, repo, token) -> UnitOwnerRepo:
    """
    Handles request for a single organization/user repository.
    Has no limits since it fetches data from a single repo,
    cannot use `--limit` flag with the `--repo` option.
    """
    if token:
        request_headers["Authorization"] = f"token {token}"

    url: str = f"https://api.github.com/repos/{name}/{repo}/issues?labels=good first issue"

    spinner = Halo(text="Fetching issues...", spinner="dots")
    spinner.start()

    # Make request to the API.
    response: Response = caller(url, request_headers)

    spinner.succeed("Issues fetched.")

    issues: Dict = response.json()

    # Extract rate_limit from response header.
    rate_limit: Optional[str] = dict(response.headers).get(
        "X-RateLimit-Remaining"
    )

    return helpers.unit_repo_issue_extract(issues), rate_limit


def owner_repos(name: str, token: str, limiter: Optional[int]) -> OwnerRepos:
    """
    Searches for issues in all repos under individual user or organization.
    """
    per_page: int = 20

    # Check for GitHub token.
    if token:
        request_headers["Authorization"] = f"token {token}"
        per_page = 100

    url: str = f"https://api.github.com/users/{name}/repos?per_page={per_page}"

    spinner.start()

    # Make request to the API.
    response: Response = caller(url, request_headers)

    response.raise_for_status()
    spinner.succeed("Repos fetched.")

    data: Dict = response.json()

    # Extract rate_limit from response header.
    rate_limit: Optional[str] = dict(response.headers).get(
        "X-RateLimit-Remaining"
    )

    # Base URL for individual repos.
    unit_repo_url: str = "https://api.github.com/repos/{full_name}/issues?labels=good first issue"

    # Format Base URL with full_name of individual repo.
    all_repo_urls: List = [
        unit_repo_url.format(full_name=item.get("full_name")) for item in data
    ]

    # Send concurrent requests to fetch repo data.
    issues: List = concurrent_requests(all_repo_urls, request_headers, limiter)

    # No issues found.
    if not issues:
        return False, rate_limit

    issue_data = map(helpers.extract_issues, issues)

    return list(issue_data), rate_limit


def concurrent_requests(
    all_repo_urls: List, request_headers: Dict, limiter: Optional[int]
) -> List:
    """
    Send concurrent requests to the repo urls fetched.
    """
    issues: List = []

    spinner = Halo(text="Looking for good first issues...", spinner="dots")
    spinner.start()

    # Send concurrent requests to the API.
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        submit = [
            executor.submit(
                caller,
                url,
                request_headers,
            )
            for url in all_repo_urls
        ]

        for future in concurrent.futures.as_completed(submit):
            if limiter and len(issues) >= limiter:
                break

            # Ignore empty values.
            if not future.result():
                continue

            issues.extend(future.result().json())

    spinner.succeed("Parsing complete.")

    return issues[:limiter]


def caller(url: str, request_headers, timeout: int = 30) -> Response:
    """
    Call the API end point.

    > Centralized requests handler, all network exceptions captured here.
    """
    response: requests.models.Response = requests.get(
        url, timeout=timeout, headers=request_headers
    )
    try:
        response.raise_for_status()
    except requests.exceptions.ReadTimeout:
        spinner.fail("Error")
        console.print(
            "\n Network connection timeout.:construction:",
            style="bold red",
        )

        sys.exit()
    except requests.exceptions.HTTPError:
        spinner.fail("Error")
        error = response.json().get("message")
        console.print(
            f"\n Error: {error}.:warning:",
            style="bold red",
        )

        sys.exit()
    except:
        spinner.fail("Error")
        console.print(
            "\n An error has occcured. Please try again later or open a issue on GitHub.:warning:",
            style="bold red",
        )

        sys.exit()

    return response
