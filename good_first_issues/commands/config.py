import click

from good_first_issues import utils


@click.command()
def config():
    """
    Prompt user to enter Github Fine-grained Personal Access Token.

    Generate token here:

        https://github.com/settings/tokens?type=beta
    """
    token: str = click.prompt(
        "Enter your GitHub Access Token (hidden)", hide_input=True
    )

    utils.add_credential(token)
