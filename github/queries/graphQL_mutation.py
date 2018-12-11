class ViewerMutation:
    __slots__ = 'payload', 'viewer_id', 'query'

    """
    Query structure:
    mutation ACTION {
    addReaction(input:{INPUT}) {
    clientMutationId
    }  }

  Payload structure:
   ('ACTION', {'param': 'value', 'param2': 'value2'})
    """

    def __init__(self, payload: tuple):
        self.payload = payload
        self.viewer_id = None
        self.query = None

    @staticmethod
    def obtain_viewer_id_query():
        return {'query': '{viewer {id}}'}

    @staticmethod
    def obtain_viewer_login_query():
        return {'query': '{viewer {login}}'}

    @staticmethod
    def obtain_repository_id(repository_name: str):
        return {'query': f'{{viewer {{repository (name: {repository_name}) {{ id }} }} }}'}

    def construct_query(self):
        attributes_as_string = [f'{k}: "{v}"' for k, v in self.payload[1].items()]
        self.query = f'mutation {{ {self.payload[0]}(input: ' \
            f'{{ {", ".join(attr for attr in attributes_as_string) } }}) ' \
            f'{{ clientMutationId }} }}'

    def __dict__(self):
        return {'query': self.query}
