"""Entrypoint of the CLI"""
from typing import List, Optional

import click
from rich.console import Console

from . import utils
from .rest.commands import get
from .graphql.commands import gql


console = Console(color_system="auto")


@click.group()
def cli():
    """
    Get good first issues to start hacking.

    Using REST API:

    $ gfi get ...

    Using GraphQL: (Requires Authentication Token)

    $ gfi gql ...

    """
    pass


# Add sub-commands for REST API and GraphQL.
cli.add_command(get)
cli.add_command(gql)


@cli.command()
@click.option("--gql", is_flag=True, help="Rate limit for GraphQL API.")
def rate_limit(gql: bool):
    """
    Display GitHub API rate limit.
    """
    if gql:
        rate_limit = utils.gql_rate_limit()
    else:
        rate_limit = utils.rate_limit()

    console.print(
        f"Remaining requests:dash:: {rate_limit}", style="bold green"
    )


@cli.command()
def config():
    """
    Prompt user to enter Github Personal Access Token.
    """
    token: str = click.prompt(
        "Enter your GitHub Access Token (hidden)", hide_input=True
    )

    utils.add_credential(token)
