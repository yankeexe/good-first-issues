<p align="center">
  <img src="https://i.imgur.com/vTgsBoQ.png" width="100" alt="Good First Issues"/></a>
</p>

<h1 align="center"><strong> Good First Issues</strong> </h1>
<p align="center"><strong>Find good first issues right from your CLI!</strong></p>

<p align="center">
<img src="https://img.shields.io/pypi/v/good-first-issues" />
<img src="https://img.shields.io/pypi/pyversions/good-first-issues" />
<img src="https://img.shields.io/pypi/l/good-first-issues"/>
<img src="https://static.pepy.tech/badge/good-first-issues"/>

</p>

## Install Good First Issues

Requires Python 3.9 or higher.

```bash
$ pip3 install good-first-issues --upgrade
```

The CLI uses the alias `gfi` to run commands.

<img src="https://i.imgur.com/UM4e9vQ.png" width="800" />

## Contents

- [Install Good First Issues](#install-good-first-issues)
- [Contents](#contents)
  - [Create GitHub Personal Access Token](#create-github-personal-access-token)
- [Usage](#usage)
  - [Search for issues](#search-for-issues)
    - [Query all repos in an organization](#query-all-repos-in-an-organization)
    - [Query a single repo in an organization](#query-a-single-repo-in-an-organization)
    - [Query all repos in a user profile](#query-all-repos-in-a-user-profile)
    - [Query a single repo in a user profile.](#query-a-single-repo-in-a-user-profile)
  - [Search for Hacktoberfest approved issues](#search-for-hacktoberfest-approved-issues)
    - [Query all repos with topic `hacktoberfest`](#query-all-repos-with-topic-hacktoberfest)
    - [Query all repos with topic 'hacktoberfest' in an organization or in a user profile](#query-all-repos-with-topic-hacktoberfest-in-an-organization-or-in-a-user-profile)
  - [Changing output limits](#changing-output-limits)
  - [Viewing issues on browser](#viewing-issues-on-browser)
- [Contributing](#contributing)

### Create GitHub Personal Access Token

The CLI requires GitHub Personal Access Token to make requests to the GitHub API.

> Get [GitHub Fine-grained Personal Access Token](https://github.com/settings/tokens?type=beta)

You can add a Description to your token, select "Public Repositories (read-only)" and select _Generate token_.

**Provide token to CLI:**

```bash
$ gfi config
```

Token is stored locally on `/home/<username>/.gfi/good-first-issues` file.

**Token in envrionment variable:**

Store the token with the name `GFITOKEN` in your environment.

## Usage

GitHub provides API to fetch user and organization data. [Personal Access Token](#create-github-personal-access-token) is required for authentication and data fetching.

### Search for issues

To look for issues, use the `gfi search` command.

#### Query all repos in an organization

```bash
$ gfi search "rust-lang"
```

> <details><summary><strong>Demo</strong></summary>
> <img src = "https://i.imgur.com/B8zRd1z.gif" width="700" alt="demo of timezone cli search" />

</details>

#### Query a single repo in an organization

```bash
$ gfi search "facebook" --repo "jest"
```

> <details><summary><strong>Demo</strong></summary>
> <img src = "https://i.imgur.com/XayYGEd.gif" width="700" alt="demo of timezone cli search" />

</details>

#### Query all repos in a user profile

```bash
$ gfi search "yankeexe" --user
```

> <details><summary><strong>Demo</strong></summary>
> <img src = "https://i.imgur.com/LnPrk4A.gif" width="700" alt="demo of timezone cli search" />

</details>

#### Query a single repo in a user profile.

`--user` flag not required here.

```bash
$ gfi search "yankeexe" --repo "good-first-issues"
```

> <details><summary><strong>Demo</strong></summary>
> <img src = "https://i.imgur.com/ywGT9VQ.gif" width="700" alt="demo of timezone cli search" />

</details>

### Search for Hacktoberfest approved issues

#### Query all repos with topic `hacktoberfest`

```bash
$ gfi search --hacktoberfest

$ gfi search -hf
```

### Search for issues within a certain period

By default, no period is set and users are shown whatever data is fetched from the GitHub API.

To filter good first issues within a certain period, use the following commands:

```bash

# Query all organization repos
$ gfi search "rust-lang" -p "30 hours"

# Query a specific repo in an organization
$ gfi search "rust-lang" --repo "rust" -p "30 mins"

# Query repos with the topic hacktoberfest
$ gfi search -hf -p "100 days"

# Query all user repos
$ gfi search "yankeexe" --user -p "600 hrs"

# Query a specific repo of a user
$ gfi search "yankeexe" --user --repo "good-first-issues" -p "600 days"
```

```bash
# Example Usage:
--period 1 m,min,mins,minutes

--period 2 h,hr,hour,hours,hrs

--period 3 d,day,days

```


> <details><summary><strong>Demo</strong></summary>
> <img src = "https://i.imgur.com/6Ch5BFG.gif" width="700" alt="demo of timezone cli search" />

</details>

#### Query all repos with topic 'hacktoberfest' in an organization or in a user profile

Query all repos with topic 'hacktoberfest' in an organization.

```bash
$ gfi search "facebook" --hacktoberfest
```

> <details><summary><strong>Demo</strong></summary>
> <img src = "https://i.imgur.com/Kj6lEMN.gif" width="700" alt="demo of timezone cli search" />

</details>

Query all repos with topic 'hacktoberfest' in a user profile.
`--user` flag not required here.

```bash
$ gfi search "yankeexe" --hacktoberfest
```

> <details><summary><strong>Demo</strong></summary>
> <img src = "https://i.imgur.com/vrgr8ju.gif" width="700" alt="demo of timezone cli search" />

</details>

### Changing output limits

The output is limited to display 10 issues by default. Use `--limit` flag to set the number of issues for output or `--all` for no limits.

Limit the issues to 12

```bash
$ gfi search "facebook" --limit 12
```

> <details><summary><strong>Demo</strong></summary>
> <img src = "https://i.imgur.com/WdXhA4Z.gif" width="700" alt="demo of timezone cli search" />

</details>

View all issues found.

```bash
$ gfi search "rust-lang" --all
```

### Viewing issues on browser

It's hard to navigate through all the issues when you have the `--all` flag enabled, you can view the issues on your browser with ease using the `--web` flag.

```bash
$ gfi search "facebook" --all --web
```

> <details><summary><strong>Demo</strong></summary>
> <img src = "https://i.imgur.com/AukVqdk.gif" width="700" alt="demo of timezone cli search" />

</details>

## Contributing

For guidance on setting up a development environment and how to make a contribution to `good-first-issues`, see the [contributing guidelines](https://github.com/yankeexe/good-first-issues/blob/master/CONTRIBUTING.md).
