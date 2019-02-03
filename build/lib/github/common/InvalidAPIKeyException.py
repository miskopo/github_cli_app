class InvalidAPIKeyException(Exception):
    def __init__(self, *args):
        super(InvalidAPIKeyException, self).__init__(*args)
