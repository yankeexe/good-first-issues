"""GraphQL queries"""

core_query = """
query SearchGoodFirstIssues($searchQuery: String!, $limit: Int!) {
  rateLimit {
    limit
    cost
    remaining
    resetAt
  }
  search(query: $searchQuery, type: ISSUE, first: $limit) {
    issueCount
    nodes {
      ... on Issue {
        title
        url
        createdAt
        author {
          login
        }
        repository {
          name
          owner {
            login
          }
        }
        labels(first: 3) {
          nodes {
            name
          }
        }
        number
        state
      }
    }
  }
}
"""

# `first: 2` = Fetch only 2 issues from each repos with the topic hacktoberfest
search_query: str = """
query search($queryString: String!){
  search(type: REPOSITORY, query: $queryString, first: 50) {
    edges {
      node {
        ... on Repository {
          url
          issues(filterBy: { states: OPEN, labels: "good first issue" }, first: 2) {
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
