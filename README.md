<p align="center">
  <img src="https://i.imgur.com/vTgsBoQ.png" width="100" alt="Good First Issues"/>
</p>

<h1 align="center">
  <strong> Good First Issues</strong>
</h1>

<p align="center">
  <strong>Find good first issues right from your CLI!</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/pypi/v/good-first-issues?style=flat-square&color=black"/>
  <img src="https://img.shields.io/pypi/pyversions/good-first-issues?style=flat-square&color=black" />
  <img src="https://img.shields.io/pypi/l/good-first-issues?style=flat-square&color=black"/>
  <img src="https://static.pepy.tech/badge/good-first-issues"/>
</p>

## 📦 Installation

Requires **Python 3.9 or higher**.

```bash
$ pip install good-first-issues --upgrade

# Using uvx
$ uvx --from good-first-issues gfi
```

The CLI uses the alias `gfi` to run commands.

### ✓ Verify Installation

After installation, you can verify that `gfi` is installed correctly by checking the version:

```bash
$ gfi version
```

This should display the installed version of good-first-issues.

<img src="https://i.imgur.com/UM4e9vQ.png" width="800" />

## Contents

- [📦 Installation](#-installation)  
- [🔑 Create GitHub Personal Access Token](#-create-github-personal-access-token)
- [🚀 Usage](#-usage)
  - [🏢 Query all repos in an organization](#-query-all-repos-in-an-organization)
  - [📦 Query a single repo in an organization](#-query-a-single-repo-in-an-organization)
  - [👨‍💻 Query all repos in a user profile](#-query-all-repos-in-a-user-profile)
  - [📦 Query a single repo in a user profile](#-query-a-single-repo-in-a-user-profile)
  - [🐙 Query all repos with topic `hacktoberfest`](#-query-all-repos-with-topic-hacktoberfest)
    - [Query all repos with topic 'hacktoberfest' in an organization or in a user profile](#query-all-repos-with-topic-hacktoberfest-in-an-organization-or-in-a-user-profile)
  - [📏 Search for issues within a certain period](#-search-for-issues-within-a-certain-period)
  - [⚖️ Limit output](#️-limit-output)
  - [🌐 View issues on browser](#-view-issues-on-browser)
  - [👀 Show the CLI version](#-show-the-cli-version)
- [🔨 Contributing](#-contributing)

### 🔑 Create GitHub Personal Access Token

The CLI requires GitHub Personal Access Token to make requests to the GitHub API.

> Get [GitHub Fine-grained Personal Access Token](https://github.com/settings/tokens?type=beta)

You can add a Description to your token, select "Public Repositories (read-only)" and select _Generate token_.

When you run the CLI for the first time, you'll be prompted for the GitHub Personal Access Token.

The token is stored locally in `~/.gfi/good-first-issues` file.

## 🚀 Usage

### 🏢 Query all repos in an organization

```bash
$ gfi search "kubernetes"
```

> <details>
> <summary>
> <strong>Demo</strong>
> </summary>
>
> <img src="https://i.imgur.com/OmfN76J.gif" width="700" alt="demo of timezone cli search" />
>
> </details>

### 📦 Query a single repo in an organization

```bash
$ gfi search "rust-lang" --repo "rust"
```

### 👨‍💻 Query all repos in a user profile

```bash
$ gfi search "yankeexe" --user
```

### 📦 Query a single repo in a user profile

```bash
$ gfi search "yankeexe" --user --repo "good-first-issues"
```

### 🐙 Query all repos with topic `hacktoberfest`

```bash
$ gfi search -hf
```

#### Query all repos with topic 'hacktoberfest' in an organization or in a user profile

```bash
# Query for an organization
$ gfi search "do-community" -hf

# Query for a user profile
$ gfi search "yankeexe" -hf --user
```

### 📏 Search for issues within a certain period

By default, the issues are filtered within 1 day. You can provide filter period using `--period` flag.

Pass period in minutes, hours or days.

```bash
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

### ⚖️ Limit output

The output is limited to display 10 issues by default. Use `--limit` flag to set the number of issues for output or `--all` for no limits.

Limit the issues to 12

```bash
$ gfi search "facebook" --limit 12
```

> <details>
> <summary>
> <strong>Demo</strong>
> </summary>
>
> <img src="https://i.imgur.com/WdXhA4Z.gif" width="700" alt="demo of timezone cli search" />
>
> </details>

View all issues found.

```bash
$ gfi search "rust-lang" --all
```

### 🌐 View issues on browser

It's hard to navigate through all the issues when you have the `--all` flag enabled, you can view the issues on your browser with ease using the `--web` flag.

```bash
$ gfi search "facebook" --all --web
```

> <details>
> <summary>
> <strong>Demo</strong>
> </summary>
>
> <img src="https://i.imgur.com/AukVqdk.gif" width="700" alt="demo of timezone cli search" />
>
> </details>

### 👀 Show the CLI version

```bash
$ gfi version
```

## 🔨 Contributing

For guidance on setting up a development environment and how to make a contribution to `good-first-issues`, see the [contributing guidelines](https://github.com/yankeexe/good-first-issues/blob/master/CONTRIBUTING.md).
