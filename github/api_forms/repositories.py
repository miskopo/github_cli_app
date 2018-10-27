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
        'repositories (first: 30) { '
        'totalCount pageInfo { hasNextPage endCursor } edges { node { name url sshUrl} } } } '
        '}'
}
