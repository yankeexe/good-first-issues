<p align="center">
  <img src="https://i.imgur.com/vTgsBoQ.png" width="100" alt="Good First Issues"/>
</p>

<h1 align="center"><strong> Good First Issues</strong> </h1>
<p align="center"><strong>Find good first issues right from your CLI!</strong></p>

<p align="center">
<img src="https://img.shields.io/pypi/v/good-first-issues?style=flat-square&color=black"/>
<img src="https://img.shields.io/pypi/pyversions/good-first-issues?style=flat-square&color=black" />
<img src="https://img.shields.io/pypi/l/good-first-issues?style=flat-square&color=black"/>
<img src="https://static.pepy.tech/badge/good-first-issues"/>
</p>

## 📦 Installation

> Requires **Python 3.9 or higher**.

```bash
$ pip install good-first-issues --upgrade
```

The CLI uses the alias `gfi` to run commands.

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
  - [📏 Search for issues within a certain period](#-search-for-issues-within-a-certain-period)
  - [⚖️ Limit output](#%ef%b8%8f-limit-output)
  - [🌐 View issues on browser](#-view-issues-on-browser)
  - [👀 Show the CLI version](#-show-the-cli-version)
  - [📃 Enable Logging](#-enable-logging)
- [🛠️ Contributing](#-contributing)

### 🔑 Create GitHub Personal Access Token

The CLI requires GitHub Personal Access Token to make requests to the GitHub API.

> Get [GitHub Fine-grained Personal Access Token](https://github.com/settings/tokens?type=beta)

You can add a Description to your token, select "Public Repositories (read-only)" and select _Generate token_.

**Provide token to CLI:**

```bash
$ gfi config
```

Token is stored locally on `/home/<username>/.gfi/good-first-issues` file.

**Token in environment variable:**

Store the token with the name `GFITOKEN` in your environment.

## 🚀 Usage

GitHub provides API to fetch user and organization data. [Personal Access Token](#create-github-personal-access-token) is required for authentication and data fetching.

### ⚡ Enable Logging

For debugging and tracking API usage, logging can be enabled with the `--log` flag.

```bash
$ gfi search "rust-lang" --log
```

Logs are saved in `/home/<username>/.gfi/logs.txt`.

### 🏢 Query all repos in an organization

```bash
$ gfi search "rust-lang"
```

### 👀 Show the CLI version

```bash
$ gfi version
```

## 🛠️ Contributing

For guidance on setting up a development environment and how to make a contribution to `good-first-issues`, see the [contributing guidelines](https://github.com/yankeexe/good-first-issues/blob/master/CONTRIBUTING.md).
