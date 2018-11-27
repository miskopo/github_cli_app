from .graphQL_query import ViewerQuery

query = '{ repositories (first: 50) { totalCount pageInfo { endCursor } edges { node { name url sshUrl} } } }'
list_repositories = ViewerQuery({'repositories': ['name', 'url', 'sshUrl']})


list_user_repositories = {
    'query':
        '{ '
        'user (login: "username_placeholder") { '
        'repositories (first: count_placeholder) { '
        'totalCount pageInfo { hasNextPage endCursor } '
        'edges { '
        'node { '
        'name url sshUrl} } } } '
        '}'
}

get_total_number_of_repositories = {
    'query':
        '{ '
        'user (login: "username_placeholder") { '
        'repositories (first: 1) { '
        'totalCount } '
        '}'
        '}'
}

ql_list_user_repositories = {
    'query($username:String!)': {
        'user(login: $username)': {
            'repositories(first: 30)': {
                'edges': {
                    'node': {
                        'name'
                    }
                }
            }
        }
    },
    'variables': {'username': "cathelyn"}
}

