import os
import requests

def execute_graphql_query(query: str, variables: dict = None) -> dict:
    """
    Execute a GraphQL query against GitHub API
    
    Args:
        query (str): GraphQL query string
        variables (dict): Query variables
        
    Returns:
        dict: Query response
    """
    headers = {
        "Authorization": f"Bearer {get_github_token()}",
        "Content-Type": "application/json",
    }
    
    response = requests.post(
        "https://api.github.com/graphql",
        json={"query": query, "variables": variables},
        headers=headers
    )
    
    if response.status_code != 200:
        raise Exception(f"Query failed with status code: {response.status_code}")
        
    result = response.json()
    if "errors" in result:
        raise Exception(f"Query failed with errors: {result['errors']}")
        
    return result

def get_github_token() -> str:
    """
    Get GitHub token from environment variable
    """
    import os
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise Exception("GITHUB_TOKEN environment variable is not set")
    return token

def fetch_repositories(org_name: str, cursor: str = None) -> dict:
    """
    Fetch repositories with pagination support
    """
    query = """
    query($org: String!, $cursor: String) {
        organization(login: $org) {
            repositories(first: 100, after: $cursor) {
                pageInfo {
                    hasNextPage
                    endCursor
                }
                nodes {
                    name
                    description
                    url
                }
            }
        }
    }
    """
    
    variables = {
        "org": org_name,
        "cursor": cursor
    }
    
    return execute_graphql_query(query, variables)

def display_repositories(repositories: list):
    """
    Display repository information to user
    """
    for repo in repositories:
        print(f"Name: {repo['name']}")
        print(f"Description: {repo['description']}")
        print(f"URL: {repo['url']}")
        print("-" * 50)

def handle_pagination(org_name: str):
    """
    Handle pagination flow
    """
    cursor = None
    
    while True:
        result = fetch_repositories(org_name, cursor)
        repos = result['data']['organization']['repositories']
        
        display_repositories(repos['nodes'])
        
        if repos['pageInfo']['hasNextPage']:
            should_continue = input("\nWould you like to see more repositories? (y/n): ")
            if should_continue.lower() != 'y':
                break
            cursor = repos['pageInfo']['endCursor']
        else:
            print("\nNo more repositories to display.")
            break 

def main():
    """
    Main function to run the GitHub repository fetcher
    """
    try:
        org_name = input("Enter GitHub organization name: ")
        print(f"\nRepositories for {org_name} organization:\n")
        handle_pagination(org_name)
    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    main() 