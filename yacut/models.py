import random
import re
from datetime import datetime as dt
from http import HTTPStatus

from yacut.constants import (
    ALLOWED_SYMBOLS, CUSTOM_URL_LENGHT, GENERATED_SHORT_LENGTH, MAX_ATTEMPTS,
    ORIGINAL_URL_LENGTH
)

from . import db

GENARATE_SHORT_ERROR = 'Не удалось сгенерировать короткую ссылку'
SHORT_EXISTS = 'Предложенный вариант короткой ссылки уже существует.'
UNCORRECT_NAME = 'Указано недопустимое имя для короткой ссылки'
UNCORRECT_ID = 'Указанный id не найден'


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(ORIGINAL_URL_LENGTH))
    short = db.Column(db.String(CUSTOM_URL_LENGHT), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=dt.utcnow)

    def add_url_mapping(**kwargs):
        if 'form' in kwargs:
            form = kwargs['form']
            original = form.original_link.data
            short = (
                form.custom_id.data if form.custom_id.data
                else URLMap.generate_short()
            )
            if URLMap.query.filter_by(short=short).first():
                raise ValueError(SHORT_EXISTS)
            if not re.match(f'^[{ALLOWED_SYMBOLS}]+$', short):
                raise ValueError(UNCORRECT_NAME)
            url_mapping = URLMap(
                original=original,
                short=short
            )
        elif 'data' in kwargs:
            data = kwargs['data']
            if 'custom_id' in data and data['custom_id']:
                if URLMap.query.filter_by(short=data['custom_id']).first():
                    raise ValueError(SHORT_EXISTS)
                if (len(data['custom_id']) > CUSTOM_URL_LENGHT
                        or not re.match(
                            f'^[{ALLOWED_SYMBOLS}]+$', data['custom_id']
                )):
                    raise ValueError(UNCORRECT_NAME)
            short = (
                URLMap.generate_short()
                if 'custom_id' not in data or not data['custom_id']
                else data.get('custom_id')
            )
            url_mapping = URLMap(
                original=data['url'],
                short=short
            )
        db.session.add(url_mapping)
        db.session.commit()
        return url_mapping

    @staticmethod
    def find_original_or_404(short):
        return URLMap.query.filter_by(short=short).first_or_404().original

    @staticmethod
    def find_url_mapping(short_id):
        url_mapping = URLMap.get_url_mapping(short_id)
        if not url_mapping:
            raise ValueError(UNCORRECT_ID)
        return url_mapping

    @staticmethod
    def get_url_mapping(short):
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def generate_short():
        for _ in range(MAX_ATTEMPTS):
            short = ''.join(
                random.choices(ALLOWED_SYMBOLS, k=GENERATED_SHORT_LENGTH)
            )
            if not URLMap.get_url_mapping(short):
                return short
        raise ValueError(GENARATE_SHORT_ERROR)
