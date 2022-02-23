import click
from rich.console import Console

from good_first_issues import utils

console = Console(color_system="auto")


@click.command("rate-limit")
def rate_limit():
    """
    Display GitHub API rate limit.
    """
    rate_limit = utils.gql_rate_limit()

    console.print(f"Remaining requests:dash:: {rate_limit}", style="bold green")
