"""
Get good first issues to start hacking.

Using REST API:

$ gfi get ...

Using GraphQL: (Requires Authentication Token)

$ gfi gql ...
"""
from good_first_issues.utils import rate_limit, config
from good_first_issues.graphql.commands import gql
from good_first_issues.rest.commands import get
from cliche import main
