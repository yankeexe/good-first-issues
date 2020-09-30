"""GraphQL queries"""

org_query: str = """
query getIssues($name: String!) {
  organization(login: $name) {
    repositories(first: 100) {
      edges {
        node {
          name
          issues(first: 100, states: OPEN, labels: "good first issue") {
            edges {
              node {
                title
                url
              }
            }
          }
        }
      }
    }
  }
  rateLimit {
    remaining
  }
}
"""

user_query: str = """
query getIssues ($name: String!) {
  user(login: $name) {
    repositories(first: 100) {
      edges {
        node {
          name
          issues(first: 100, states: OPEN, labels: "good first issue") {
            edges {
              node {
                title
                url
              }
            }
          }
        }
      }
    }
  }
  rateLimit {
    remaining
  }
}

"""

repo_query: str = """
query getIssues($name: String!, $owner: String!) {
  repository(name: $name, owner: $owner) {
    issues(filterBy: { states: OPEN, labels: "good first issue" }, first: 100) {
      edges {
        node {
          title
          url
        }
      }
    }
  }
  rateLimit {
    remaining
  }
}
"""

rate_limit_query: str = """
{
  rateLimit {
    remaining
  }
}
"""
