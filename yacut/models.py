import random
import re
from datetime import datetime as dt

from yacut.constants import (
    ALLOWED_SYMBOLS, CUSTOM_URL_LENGHT, GENERATED_SHORT_LENGTH, MAX_ATTEMPTS,
    ORIGINAL_URL_LENGTH, REGEX
)
from . import db

GENARATE_SHORT_ERROR = 'Не удалось сгенерировать короткую ссылку'
SHORT_EXISTS = 'Предложенный вариант короткой ссылки уже существует.'
UNCORRECT_NAME = 'Указано недопустимое имя для короткой ссылки'


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(ORIGINAL_URL_LENGTH))
    short = db.Column(db.String(CUSTOM_URL_LENGHT), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=dt.utcnow)

    def add_url_mapping(original, short):
        if URLMap.get(short):
            raise ValueError(SHORT_EXISTS)
        if not re.match(REGEX, short):
            raise ValueError(UNCORRECT_NAME)
        if (len(short) > CUSTOM_URL_LENGHT
                or not re.match(REGEX, short)):
            raise ValueError(UNCORRECT_NAME)
        url_mapping = URLMap(
            original=original,
            short=short
        )
        db.session.add(url_mapping)
        db.session.commit()
        return url_mapping

    @staticmethod
    def get_or_404(short):
        return URLMap.query.filter_by(short=short).first_or_404().original

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
