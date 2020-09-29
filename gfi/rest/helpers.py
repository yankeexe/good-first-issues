"""Helper functions for the REST API mode."""
from typing import List, Dict, Union

from halo import Halo
from rich.console import Console


console = Console(color_system="auto")

headers: List = ["title", "html_url"]


def unit_repo_issue_extract(issues: List) -> Union[List, bool]:
    """
    Extract issues from unit or individual repos.
    """
    data_store: List = []

    spinner = Halo(text="Looking for good first issues...", spinner="dots")
    spinner.start()

    # Parse issue data
    for issue in issues:
        store = [issue.get(col) for col in headers]
        data_store.append(store)

    spinner.succeed("Parsing complete.")

    # No issues found.
    if not data_store:
        return False

    return data_store


def extract_issues(issue: Dict) -> List:
    """
    Extract issues from the API response.
    """
    return [issue.get(col) for col in headers]
