import random

from yacut.constants import ALLOWED_SYMBOLS, LENGTH
from yacut.models import URLMap


def check_short(short):
    return all(symbol in ALLOWED_SYMBOLS for symbol in short)


def get_short():
    short = ''.join(random.choices(ALLOWED_SYMBOLS, k=LENGTH))
    return (
        short if not URLMap.query.filter_by(short=short).first()
        else get_short()
    )
