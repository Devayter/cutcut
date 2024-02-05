import string

ALLOWED_SYMBOLS = string.ascii_letters + string.digits
SHORT_LENGHT = 16
GENERATED_SHORT_LENGTH = 6
ORIGINAL_LENGTH = 512
MAX_ATTEMPTS = 3

SHORT_ROUTE = 'open_link'
REGEX = f'^[{ALLOWED_SYMBOLS}]+$'
