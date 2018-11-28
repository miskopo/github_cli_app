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
    def obtain_user_id_query():
        return {'query': '{viewer {id} }'}

    def construct_query(self):
        self.query = f'createProject(input: {{ ownerID: {self.viewer_id}, name: "Test name"}}) {{ clientMutationId}}'
