"""Entrypoint of the CLI"""
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--language", help="Filter by programming language")
parser.add_argument("--keyword", help="Filter by keyword in title or description")

import click
from rich.console import Console

from good_first_issues.commands import (
    config,
    rate_limit,
    search,  # THIS IS ALREADY THE COMMAND
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
cli.add_command(search)  # <-- command already implemented in search.py
cli.add_command(rate_limit)
cli.add_command(version)