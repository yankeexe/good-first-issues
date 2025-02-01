import click
from importlib.metadata import version, PackageNotFoundError


@click.command("version")
def show_version():
    """Shows what version you are running"""
    try:
        ver = version("good-first-issues")
        click.echo(f"good-first-issues: {ver}")
    except PackageNotFoundError:
        click.echo(
            "Package not found. Make sure good-first-issues is installed.", err=True
        )
        raise click.Abort()
