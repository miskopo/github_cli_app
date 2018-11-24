class GraphQLQuery:
    __slots__ = 'payload', 'variables'

    def __init__(self, payload, variables=None):
        self.payload = payload
        self.variables = variables

    def __str__(self):
        if not self.variables:
            return f"'query': {self.payload}"
        else:
            return f"'query()'"

    def __dict__(self):
        return {'query': f'{self.payload}'}


class GraphQLUserQuery(GraphQLQuery):
    def __init__(self, payload, variables=None):
        super(GraphQLUserQuery, self).__init__()