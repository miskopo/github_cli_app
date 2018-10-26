list_repositories = {
    'query':
        '{ '
        'viewer { '
        'repositories (first: 30) { '
        'totalCount pageInfo { hasNextPage endCursor } edges { node { name url sshUrl} } } } '
        '}'
}
