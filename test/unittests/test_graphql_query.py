from pytest import raises

from github.queries.graphQL_query import ViewerQuery, UserQuery, BaseQueryClass

MAX_RESULTS = 50


def test_viewer_query():
    viewer_query = ViewerQuery(payload=('repositories', ['name', 'sshUrl', 'url']))
    assert isinstance(viewer_query, BaseQueryClass)

    viewer_query.construct_query()
    assert viewer_query.query == f'{{viewer {{ repositories (first: {MAX_RESULTS}) {{ totalCount pageInfo ' \
        f'{{ endCursor }} edges {{ node {{ name sshUrl url }} }} }} }} }}'


def test_user_query():
    user_query = UserQuery(payload=('repositories', ['name', 'sshUrl', 'url']), username="dummy_user")
    assert isinstance(user_query, BaseQueryClass)

    with raises(TypeError):
        user_query.username = 42

    user_query.username = "dummy_user_2"
    assert user_query.username == "dummy_user_2"

    user_query.construct_query() \

    assert user_query.query == f'{{ user(login: dummy_user_2)  {{ repositories (first: {MAX_RESULTS}) ' \
        f'{{ totalCount pageInfo ' \
        f'{{ endCursor }} edges {{ node {{ name sshUrl url }} }} }} }} }}'
