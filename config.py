# You have to have your own unique two values for API_KEY and API_SECRET
# Obtain yours from https://www.last.fm/api/account/create for Last.fm
import logging

APP_CONFIG = {
    'lastfm': {
        'config': {
            'api': {
                'app_name': 'lastfm',
                'key': '<YOUR_KEY>',
                'secret': '<YOUR_SECRET>',
                'username': '<YOUR_USERNAME>',
                'artists_search_limit': 1000,
                'play_count': 1
            }
        },
    }
}

WHITE = "\x1b[1m"
GREY = "\x1b[38;20m"
YELLOW = "\x1b[33;20m"
RED = "\x1b[31;20m"
BOLD_RED = "\x1b[31;1m"
RESET = "\x1b[0m"


# partial code obtained from: https://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output

class CustomFormatterBase(logging.Formatter):
    def __init__(self, pattern: str):
        super().__init__()
        self.pattern = pattern

    def formats(self):
        return {
            logging.DEBUG: GREY + self.pattern + RESET,
            logging.INFO: WHITE + self.pattern + RESET,
            logging.WARNING: YELLOW + self.pattern + RESET,
            logging.ERROR: RED + self.pattern + RESET,
            logging.CRITICAL: BOLD_RED + self.pattern + RESET
        }


class CustomLoggingFormatter(CustomFormatterBase):
    def __init__(self, pattern: str):
        super().__init__(pattern=pattern)

    def format(self, record):
        log_fmt = self.formats().get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
