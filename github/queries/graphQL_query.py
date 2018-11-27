from abc import ABC


class GraphQLQuery(ABC):
    __slots__ = 'payload', 'variables', 'query'

    def __str__(self):
        pass

    def __dict__(self):
        return {'query': self.query}


class ViewerQuery(GraphQLQuery):

    def __init__(self, payload: dict):
        self.payload = payload
        self.query = None

    def construct_query(self):
        self.query = f'{{viewer {{ {list(self.payload.keys())[0]} (first: 50) {{ totalCount pageInfo ' \
            f'{{ endCursor }} edges {{ node {{ {" ".join(item for item in list(self.payload.values())[0])} ' \
            f'}} }} }} }} }}'


class UserQuery(GraphQLQuery):
    def __init__(self, payload: dict, username: str = None):
        self.payload = payload
        self._username = username
        self.query = None

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        if not isinstance(value, str):
            raise TypeError("Username must be string")
        self._username = value

    def construct_query(self):
        self.query = f'{{ user(login: {self.username})  {{ {list(self.payload.keys())[0]} (first: 50) ' \
            f'{{ totalCount pageInfo ' \
            f'{{ endCursor }} edges {{ node {{ {" ".join(item for item in list(self.payload.values())[0])} ' \
            f'}} }} }} }} }}'
