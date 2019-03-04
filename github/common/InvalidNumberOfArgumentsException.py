class InvalidNumberOfArgumentsException(Exception):
    def __init__(self, *args):
        super(InvalidNumberOfArgumentsException, self).__init__(*args)
