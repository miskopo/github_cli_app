from abc import abstractmethod


class BaseQueryClass:
    __slots__ = 'payload', 'query'
    MAX_RESULTS = 50

    """
    Query structure:
    query {
    user {
    OBJECT (first: N) { totalCount pageInfo {endCursor} edges { node { ATTRIBUTES } } } } } 

    Payload structure:
    ('OBJECT', [ATTRIBUTE1, ATTRIBUTE2, ATTRIBUTE3])
    """

    def __init__(self, payload: tuple):
        self.payload = payload
        self.query = None

    def __dict__(self):
        return {'query': self.query}

    @abstractmethod
    def construct_query(self):
        raise NotImplementedError


class ViewerQuery(BaseQueryClass):
    __slots__ = 'payload', 'query'

    def __init__(self, payload: tuple):
        super().__init__(payload)

    def construct_query(self):
        self.query = f'{{viewer {{ {self.payload[0]} (first: {self.MAX_RESULTS}) {{ totalCount pageInfo ' \
            f'{{ endCursor }} edges {{ node {{ {" ".join(item for item in self.payload[1])} ' \
            f'}} }} }} }} }}'


class UserQuery(BaseQueryClass):
    __slots__ = 'payload', '_username', 'query'

    def __init__(self, payload: tuple, username: str = None):
        super().__init__(payload)
        self._username = username

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        if not isinstance(value, str):
            raise TypeError("Username must be string")
        self._username = value

    def construct_query(self):
        self.query = f'{{ user(login: {self.username})  {{ {self.payload[0]} (first: {self.MAX_RESULTS}) ' \
            f'{{ totalCount pageInfo ' \
            f'{{ endCursor }} edges {{ node {{ {" ".join(item for item in self.payload[1])} ' \
            f'}} }} }} }} }}'
