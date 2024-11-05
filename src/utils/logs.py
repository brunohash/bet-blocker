import logging

APPLICATION_NAME = "BET-BLOCKER"

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('bet-blocker.log')
file_handler.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

log_format = f'{APPLICATION_NAME} :: %(asctime)s ::  %(levelname)s -> %(message)s'

file_formatter = logging.Formatter(log_format)
file_handler.setFormatter(file_formatter)

console_formatter = logging.Formatter(log_format)
console_handler.setFormatter(console_formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)