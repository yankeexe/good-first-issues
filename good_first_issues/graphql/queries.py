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
    repositories(first: 100, ownerAffiliations: OWNER) {
      edges {
        node {
          name
          issues(filterBy: {labels: "good first issue", states: OPEN}, first: 100) {
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

search_query: str = """
query search($queryString: String!){
  search(type: REPOSITORY, query: $queryString, first: 50) {
    edges {
      node {
        ... on Repository {
          url
          issues(filterBy: { states: OPEN, labels: "good first issue" }, first: 100) {
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

rate_limit_query: str = """
{
  rateLimit {
    remaining
  }
}
"""
