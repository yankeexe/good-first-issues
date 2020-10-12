"""Entrypoint of the CLI"""
from os import name
import click
from rich.console import Console

from . import utils
from .graphql.commands import search


console = Console(color_system="auto")


@click.group()
def cli():
    """
    Get good first issues to start hacking.

    (Requires GitHub Authentication Token)

    $ gfi search

    """
    pass


# Add sub-commands for REST API and GraphQL.
cli.add_command(search)


@cli.command("rate-limit")
def rate_limit():
    """
    Display GitHub API rate limit.
    """
    rate_limit = utils.gql_rate_limit()

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
