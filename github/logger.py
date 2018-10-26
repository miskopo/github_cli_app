from logging import getLogger, DEBUG, StreamHandler, Formatter, FileHandler

logger = getLogger('github')

# Logging configuration
logger.setLevel(DEBUG)

# create console handler
console_debug_handler = StreamHandler()
console_debug_handler.setLevel(DEBUG)
file_debug_handler = FileHandler('../logs/debug.log')
file_debug_handler.setLevel(DEBUG)


# create formatter and add it to the handlers
console_debug_formatter = Formatter('>> %(message)s')
file_debug_formatter = Formatter('%(asctime)s; %(name)s; %(levelname)s;\t{:<20}\t %(message)s'.format('%(filename)s;'))

console_debug_handler.setFormatter(console_debug_formatter)
file_debug_handler.setFormatter(file_debug_formatter)

# add the handlers to the logger
logger.addHandler(console_debug_handler)
logger.addHandler(file_debug_handler)
