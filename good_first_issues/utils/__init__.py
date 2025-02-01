"""Utils for CLI"""

import datetime
import http.server
import os
import re
import shutil
import socketserver
import sys
import webbrowser
from collections import namedtuple
from pathlib import Path
from typing import Dict, Union

import click
from halo import Halo
from rich.console import Console

from good_first_issues.graphql import services
from good_first_issues.graphql.queries import rate_limit_query

console = Console(color_system="auto")


# Global variables
home_dir: str = str(Path.home())
filename: str = "good-first-issues"
credential_dir: str = f"{home_dir}/.gfi"
credential_file: str = f"{credential_dir}/{filename}"


ParsedDuration = namedtuple("ParsedDuration", ["absolute_period", "utc_date_time"])


def parse_period(duration: str) -> ParsedDuration:
    """Parses a duration string into absolute period and UTC datetime.

    Args:
        duration: String representing a duration in minutes, hours or days.
            Format: <number><unit> where unit can be:
            - m, min, mins, minutes for minutes
            - h, hr, hrs, hours for hours
            - d, day, days for days

    Returns:
        ParsedDuration: A named tuple containing:
            - absolute_period: Duration in minutes
            - utc_date_time: UTC datetime representing duration from now

    Raises:
        SystemExit: If duration string format is invalid
    """
    pattern = r"^(?P<Period>\d+)\s?(?P<Duration>m|min|mins|minutes|h|hr|hrs|hours|d|day|days)?$"
    regex = re.compile(pattern)
    match = regex.match(duration)

    if not match:
        print(
            "❌ Invalid status duration\nUse 'gfi search --help for  more information.",
            file=sys.stderr,
        )
        sys.exit(1)

    period_str = match.group("Period")
    duration_type = match.group("Duration")

    # Convert period to integer and ensure it's non-negative
    period = int(period_str)
    period = abs(period)

    if not duration_type:
        print(
            "Invalid duration.\nUse 'gfi search --help for  more information.",
            file=sys.stderr,
        )
        sys.exit(1)

    if duration_type in ["m", "min", "mins", "minutes"]:
        abs_period = period
        utc_time = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(
            minutes=period
        )
    elif duration_type in ["h", "hr", "hrs", "hours"]:
        abs_period = period * 60
        utc_time = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(
            hours=period
        )
    elif duration_type in ["d", "day", "days"]:
        abs_period = period * 60 * 24
        utc_time = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(
            days=period
        )
    else:
        print("Invalid duration type", file=sys.stderr)
        sys.exit(1)

    return ParsedDuration(
        absolute_period=abs_period,
        utc_date_time=utc_time,
    )


def print_help_msg(command):
    """
    Prints help message for passed command.
    """
    with click.Context(command) as ctx:
        click.echo(command.get_help(ctx))


def add_credential(credential: str):
    """
    Write creds to .gfi/good-first-issue file if credential argument passed.
    Delete config folder if exists and create a new one.
    """
    if os.path.exists(credential_dir):
        shutil.rmtree(credential_dir)

    os.mkdir(credential_dir)

    with open(f"{credential_file}", "w+") as cred:
        cred.write(credential.strip())

    console.print(
        f"Credentials saved to [bold blue]{credential_file}[/bold blue]:white_check_mark:",  # noqa: E501
        style="bold green",
    )


def check_credential() -> Union[str, bool]:
    """
    Check for GitHub credential in Envrionment variable
    else in config file.
    Return if exists.
    """
    if (cred := os.environ.get("GFITOKEN")) is not None:
        return cred
    elif os.path.exists(credential_file):
        with open(credential_file) as cred:
            return cred.readline()

    return False


def gql_rate_limit() -> int:
    """
    Fetch rate_limit for GraphQL API.
    """
    token: Union[str, bool] = check_credential()

    # Spinner
    spinner = Halo(text="Getting rate limit...", spinner="dots")
    spinner.start()

    payload: Dict = services.caller(token, rate_limit_query, {})

    spinner.succeed("rate limit")

    return payload["data"].get("rateLimit").get("remaining")


def web_server(html_data):
    """
    Start web server for obtained issues.
    """
    Handler = http.server.SimpleHTTPRequestHandler
    filename = "index.html"

    url_data = add_anchor_tag(html_data)
    try:
        with open(filename, "w+") as file:
            file.write(html_template.format(table=url_data))

        socketserver.TCPServer.allow_reuse_address = True

        with socketserver.TCPServer(("localhost", 0), Handler) as httpd:
            port = httpd.server_address[1]
            print("Serving at port", port)
            webbrowser.open(f"http://127.0.0.1:{port}/")
            httpd.serve_forever()

    except KeyboardInterrupt:
        print("\nServer stopped")
    finally:
        os.remove(filename)


def add_anchor_tag(html_data):
    """
    Use regex to get URL elements inside <td> tag and
    wrap them inside an anchor tag.
    """
    pattern = re.compile(r"<td>(https.+)<\/td>")
    matches = re.findall(pattern, html_data)

    for item in matches:
        url = f"<td><a target='_blank' href='{item}'>{item}</a></td>"
        html_data = re.sub(pattern, url, html_data, 1)

    return html_data


# Template for displaying issues on web.
html_template = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
<link
      href="https://fonts.googleapis.com/css2?family=Roboto&display=swap"
      rel="stylesheet"
    />
    <link
      href="https://fonts.googleapis.com/css2?family=Secular+One&display=swap"
      rel="stylesheet"
    />
    <link rel="icon" href="data:,">
    <style>
      body {{
        background-color: #afd0a9;
        font-family: "Roboto", sans-serif;
      }}

      h1 {{
        text-align: center;
        font-size: 42px;
        font-family: "Secular One", sans-serif;
        color: white;
      }}

      table {{
        border-spacing: 0px;
        width: 80%;
        margin: auto;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 5px 5px 10px gray;
      }}

      th,
      td {{
        text-align: left;
        padding: 12px;
      }}

      tr:nth-child(even) {{
        background-color: #f2f2f2;
      }}

      tr:nth-child(odd) {{
        background-color: white;
      }}

      tr:hover {{
        background-color: #c0c0c0;
      }}

      th {{
        background-color: #006e58;
        color: white;
        font-size: 18px;
        font-weight: 900;
      }}

      a {{
        color: #006e58;
      }}

      a:hover {{
        color: black;
      }}
    </style>
    <title>Good First Issues</title>
  </head>
  <body>
    <h1>Good First Issues</h1>
    {table}
  </body>
</html>

"""
