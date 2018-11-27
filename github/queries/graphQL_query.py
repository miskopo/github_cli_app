from abc import ABC


class GraphQLQuery(ABC):
    __slots__ = 'payload', 'variables'

    def __str__(self):
        pass

    def __dict__(self):
        return {'query': self.payload}


class ViewerQuery(GraphQLQuery):

    def __init__(self, payload: dict):
        self.payload = self.construct_query(payload)

    @staticmethod
    def construct_query(payload: dict):
        return f'{{viewer {{ {list(payload.keys())[0]} (first: 50) {{ totalCount pageInfo ' \
            f'{{ endCursor }} edges {{ node {{ {" ".join(item for item in list(payload.values())[0])} }} }} }} }} }}'
