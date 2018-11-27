class ViewerMutation:
    __slots__ = 'payload', 'viewer_id', 'query'

    def __init__(self, payload: dict):
        self.payload = payload
        self.viewer_id = None
        self.query = None

    @staticmethod
    def obtain_user_id_query():
        return {'query': '{viewer {id} }'}

    def construct_query(self):
        self.query = f'createProject(input: {{ ownerID: {self.viewer_id}, name: "Test name"}}) {{ clientMutationId}}'
