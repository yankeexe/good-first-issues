import click

from good_first_issues import utils


@click.command()
def config():
    """
    Prompt user to enter Github Personal Access Token.
    """
    token: str = click.prompt(
        "Enter your GitHub Access Token (hidden)", hide_input=True
    )

    utils.add_credential(token)
