list_repositories = {
    'query':
        '{ '
        'viewer { '
        'repositories (first: 50) { '
        'totalCount pageInfo { hasNextPage endCursor } edges { node { name url sshUrl} } } } '
        '}'
}

list_user_repositories = {
    'query':
        '{ '
        'user (login: "username_placeholder") { '
        'repositories (first: count_placeholder) { '
        'totalCount pageInfo { hasNextPage endCursor } edges { node { name url sshUrl} } } } '
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

create_new_repository