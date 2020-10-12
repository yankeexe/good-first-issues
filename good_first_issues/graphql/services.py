"""Services for GraphQL mode"""
import re
import sys
from click.core import Option
from urllib3.util.retry import Retry
from typing import (
    Dict,
    Iterator,
    List,
    Iterable,
    Tuple,
    Union,
    Optional,
)

import requests
from halo import Halo
from rich.console import Console
from requests.models import Response
from requests.adapters import HTTPAdapter

from good_first_issues.graphql.queries import (
    org_query,
    repo_query,
    user_query,
    search_query,
)


# Initializations
console = Console(color_system="auto")
spinner: Halo = Halo(text="Looking for good first issues...", spinner="dots")

# Type Aliases
BaseIssueEdges = Iterator[Dict[str, Dict[str, str]]]
ExtractedRepoIssues = Tuple[List[Tuple[Optional[str], Optional[str]]], int]

# Custom Error Class.
class NoToken(Exception):
    pass


def org_user_pipeline(payload: Dict, mode: str) -> Tuple[Iterable, int]:
    """
    Extract issues related to organization or a user.
    """
    # Identify owner_type for selecting proper GraphQL query.
    owner_type: str = "organization" if mode == "org" else "user"

    # Get the edges connecting to all the repositories.
    base_data: List = (
        payload["data"].get(owner_type).get("repositories").get("edges")
    )

    # Extract rate limit value.
    rate_limit: int = payload["data"].get("rateLimit").get("remaining")

    spinner.start()

    # Generator pipeline: Extract issue title and url.
    pipeline: Iterable = get_issues(get_base_issues(base_data))

    spinner.succeed("Search Complete.")

    return list(pipeline), rate_limit


def get_base_issues(data: List) -> BaseIssueEdges:
    """
    Get the edge that connects to the issue nodes.
    """
    for item in data:
        edges = item.get("node").get("issues").get("edges")

        # Remove empty list.
        if edges:
            yield edges


def get_issues(issues: BaseIssueEdges) -> Iterator[Tuple[str, str]]:
    """
    Extracts issue title and URL from the payload.
    """
    flat_list: List = [item for sublist in issues for item in sublist]

    for issue in flat_list:
        yield issue.get("node").get("title"), issue.get("node").get("url")


def extract_repo_issues(
    payload: Dict,
) -> ExtractedRepoIssues:
    """
    Extract issues with repo name specified.
    """
    # Type Aliases
    BaseData = Optional[Iterable[Dict[str, Dict[str, str]]]]
    IssueData = Tuple[Optional[str], Optional[str]]

    base_data: BaseData = (
        payload["data"].get("repository").get("issues").get("edges")
    )

    rate_limit: int = payload["data"].get("rateLimit").get("remaining")

    issues = []

    if base_data:
        for issue in base_data:
            issue_data: IssueData = (
                issue["node"].get("title"),
                issue["node"].get("url"),
            )

            issues.append(issue_data)

    return issues, rate_limit


def extract_search_results(payload: Dict) -> Tuple[Iterable, int]:
    """
    Extract issues based on search query.
    """
    # Get the edges connecting to all the repositories.
    base_data: List = payload["data"].get("search").get("edges")

    # Extract rate limit value.
    rate_limit: int = payload["data"].get("rateLimit").get("remaining")

    spinner.start()

    # Generator pipeline: Extract issue title and url.
    pipeline: Iterable = get_issues(get_base_issues(base_data))

    spinner.succeed("Search Complete.")

    return list(pipeline), rate_limit


def identify_mode(
    name: str, repo: str, user: bool, hacktoberfest: bool
) -> Tuple[str, Dict, str]:
    """
    Identify the mode based on arguments passed.

    Used for selecting:
    1. query to use
    2. variables for the query
    3. function(mode) to pass the above values to
    """
    variables: Dict = dict()

    if name and repo and user:
        query = repo_query
        variables["owner"] = name
        variables["name"] = repo
        mode: str = "repo"
    elif name and repo:
        query = repo_query
        variables["owner"] = name
        variables["name"] = repo
        mode = "repo"
    elif name and user:
        query = user_query
        variables["name"] = name
        mode = "user"
    else:
        query = org_query
        variables["name"] = name
        mode = "org"

    if hacktoberfest and not repo:
        query = search_query
        variables["queryString"] = "topic:hacktoberfest "
        if name:
            variables["queryString"] += f"user:{name}"
        mode = "search"

    if repo and hacktoberfest:
        console.print(
            "Error: --hacktoberfest or --hf cannot be used with --repo flag:x:",
            style="bold red",
        )
        sys.exit()

    return query, variables, mode


def caller(token: Union[str, bool], query: str, variables: Dict) -> Dict:
    """
    Call the GitHub GraphQL API.

    Retries if the status codes on `status_forcelist` is returned
    from the server.

    > Centralized requests handler, all network exceptions captured here.
    """
    try:
        request_headers: Dict[str, str] = dict()

        if not token:
            raise NoToken()
        else:
            request_headers["Authorization"] = f"token {token}"

        s = requests.Session()

        # Retry factors
        retries = Retry(
            total=5,
            backoff_factor=0.3,
            status_forcelist=[500, 502, 503, 504],
            method_whitelist=(["POST"]),
        )

        s.mount("https://", HTTPAdapter(max_retries=retries))

        # API Call
        response: Response = s.post(
            "https://api.github.com/graphql",
            headers=request_headers,
            json={
                "query": query,
                "variables": variables,
            },
            timeout=20,
        )

        # Check for erros in GraphQL response.
        if "errors" in response.json():
            raise Exception()

        response.raise_for_status()

    except requests.exceptions.ReadTimeout:
        spinner.fail("Error")
        console.print(
            "Network connection timeout.:construction:", style="bold red"
        )

        sys.exit()
    except requests.exceptions.HTTPError:
        spinner.fail("Error")
        error = response.json().get("message")
        console.print(
            f"Error: {error}.:x:",
            style="bold red",
        )

        sys.exit()
    except NoToken:
        spinner.fail("Error")
        console.print(
            "No GitHub Token found. Use `gfi config` to enter your token.:key:",
            style="bold red",
        )
        console.print(
            "> https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token"
        )

        sys.exit()
    except Exception:
        spinner.fail("Error")
        error_base = response.json().get("errors")[0]

        console.print(
            f"Error: {error_base.get('message')}:x:",
            style="bold red",
        )

        sys.exit()
    except:
        spinner.fail("Error")
        console.print(
            "An error has occcured. Please try again later or open an issue on GitHub.:x:",
            style="bold red",
        )

        sys.exit()

    return response.json()
