<p align="center">
  <img src="https://i.imgur.com/vTgsBoQ.png" width="100" alt="Good First Issues"/></a>
</p>

<h1 align="center"><strong> Good First Issues</strong> </h1>
<p align="center"><strong>Find good first issues right from your CLI!</strong></p>

## Install Good First Issues

Requires Python 3.6.1 or higher.

```bash
pip3 install good-first-issues
```

The CLI uses the alias `gfi` to run commands.

![good first issues](https://i.imgur.com/qudPZ0W.png)

## Contents

- [Good First Issues](#good-first-issues)
  - [Install Good First Issues](#install-good-first-issues)
    - [Create GitHub Personal Access Token:](#create-github-personal-access-token)
  - [Usage](#usage)
    - [GraphQL (recommended)](#graphql)
    - [REST API](#rest-api)
  - [Contributing](#contributing)

### Create GitHub Personal Access Token:

The CLI requires GitHub Personal Access Token to make requests to the GitHub API.

> Get [GitHub Personal Access Token](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token)

You don't have to select any scopes, add a Note for your token and select _Generate token_.

**Provide token to CLI:**

```bash
gfi config
```

Token is stored locally on `/home/<username>/.gfi/good-first-issues` file.

## Usage

GitHub provides API using both REST and GraphQL, each with 5000 requests per hour with the Personal Access Token.

You can switch between these APIs but **using the GraphQL option is faster and efficient!**

There are two ways you can get good first issues:

1. query all the repos in a user or an organization profile.
2. query a particular repo in a user or an organization profile.

### **GraphQL**

To use the GraphQL option use the `gfi gql` command.

**Query all the repos in a user or an organization profile.**

```bash
# Query all repos in an organization
gfi gql "rust-lang"

# Query all repos in a user profile
gfi gql "sindresorhus" --user
```

**Query a particular repo in a user or an organization profile.**

```bash
# Query a single repo in an organization
gfi gql "rust-lang" --repo "rust"

# Query a single repo in a user profile
# No --user flag needed.
gfi gql "sindresorhus" --repo "awesome"
```

**Query repositories with topic 'hacktoberfest'**

```bash
# Query all repos with topic 'hacktoberfest'
gfi gql --hacktoberfest

# Query all repos with topic 'hacktoberfest' in an organization or in a user profile
# No --user flag needed for user.
gfi gql "facebook" --hacktoberfest
gfi gql "yankeexe" --hacktoberfest
```

**Changing output limits**

The output is limited to display 10 issues by default. Use `--limit` flag to set the number of issues for output or `--all` for no limits.

```bash
# Limit the issues to 20
gfi gql "rust-lang" --limit 20

# View all issues found.
gfi gql "rust-lang" --all

```

**Viewing issues on browser**

<img src="https://i.imgur.com/V68FwIF.png" width="800" />

It's hard to navigate through all the issues when you have the `--all` flag enabled, you can view the issues on your browser with ease using the `--web` flag.

```bash
gfi gql "rust-lang" --all --web
```

---

### **REST API**

To use the GraphQL option use the `gfi get` command.

**Query all the repos in a user or an organization profile.**

```bash
# Query all repos in an organization
gfi get "rust-lang"

# Query all repos in a user profile
gfi get "sindresorhus"
```

**Changing output limits**

The output is limited to display 10 issues by default. Use `--limit` flag to set the number of issues for output or `--all` for no limits.

```bash
# Limit the issues to 20
gfi get "rust-lang" --limit 20

# View all issues found.
gfi get "rust-lang" --all

```

**Viewing issues on browser**

It's hard to navigate through all the issues when you have the `--all` flag enabled, you can view the issues on your browser with ease using the `--web` flag.

```bash
gfi gql "rust-lang" --all --web
```

## Contributing

For guidance on setting up a development environment and how to make a contribution to Flask, see the [contributing guidelines](https://github.com/yankeexe/good-first-issues/blob/master/CONTRIBUTING.md).
