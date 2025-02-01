"""Entrypoint of the CLI"""

import click
from rich.console import Console

from good_first_issues.commands import (
    config,
    rate_limit,
    search,
    show_version as version,
)

console = Console(color_system="auto")


@click.group()
def cli():
    """
    Get good first issues to start hacking.

    (Requires GitHub Authentication Token)

    $ gfi search

    """
    pass


cli.add_command(config)
cli.add_command(search)
cli.add_command(rate_limit)
cli.add_command(version)
