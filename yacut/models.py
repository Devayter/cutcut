import random
import re
from datetime import datetime as dt

from yacut.constants import (
    ALLOWED_SYMBOLS, SHORT_LENGHT, GENERATED_SHORT_LENGTH, MAX_ATTEMPTS,
    ORIGINAL_LENGTH, REGEX
)
from . import db

GENARATE_SHORT_ERROR = (
    'Не удалось сгенерировать короткую ссылку, повторите попытку'
)
ORIGINAL_LENGTH_ERROR = f'Длина ссылки превышает {ORIGINAL_LENGTH} символов'
SHORT_EXISTS = 'Предложенный вариант короткой ссылки уже существует.'
UNCORRECT_NAME = 'Указано недопустимое имя для короткой ссылки'


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(ORIGINAL_LENGTH))
    short = db.Column(db.String(SHORT_LENGHT), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=dt.utcnow)

    def add(original, short, need_validate=False):
        if need_validate:
            if len(original) > ORIGINAL_LENGTH:
                raise ValueError(ORIGINAL_LENGTH_ERROR)
        if short:
            if need_validate:
                if (len(short) > SHORT_LENGHT
                        or not re.match(REGEX, short)):
                    raise ValueError(UNCORRECT_NAME)
                if URLMap.get(short):
                    raise ValueError(SHORT_EXISTS)
        else:
            short = URLMap.generate_short()
        url_mapping = URLMap(
            original=original,
            short=short
        )
        db.session.add(url_mapping)
        db.session.commit()
        return url_mapping

    @staticmethod
    def get_or_404(short):
        return URLMap.query.filter_by(short=short).first_or_404()

    @staticmethod
    def get(short):
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def generate_short():
        for _ in range(MAX_ATTEMPTS):
            short = ''.join(
                random.choices(ALLOWED_SYMBOLS, k=GENERATED_SHORT_LENGTH)
            )
            if not URLMap.get(short):
                return short
        raise RuntimeError(GENARATE_SHORT_ERROR)
