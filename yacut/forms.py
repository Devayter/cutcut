from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional, Regexp

from yacut.constants import CUSTOM_URL_LENGHT, ORIGINAL_URL_LENGTH, REGEX
from yacut.models import URLMap

CUSTOM_ID_LABLE = 'Введите сокращенный вариант'
CUSTOM_ID_VALIDATOR_LENGTH = f'Длина превышает {CUSTOM_URL_LENGHT} символов'
CREATE = 'Создать'
ORIGINAL_LINK_LABLE = 'Введите оригинальную ссылку'
ORIGINAL_LINK_VALIDATOR_DATA = 'Обязательное поле'
SHORT_EXISTS = 'Предложенный вариант короткой ссылки уже существует.'
UNCORRECT_SYMBOLS = 'Недопустимые символы.'
UNCORRECT_URL = 'Некорректный URL'


class URLMapForm(FlaskForm):
    original_link = URLField(
        ORIGINAL_LINK_LABLE,
        validators=[
            DataRequired(message=ORIGINAL_LINK_VALIDATOR_DATA),
            Length(max=ORIGINAL_URL_LENGTH),
            URL(message=UNCORRECT_URL)
        ]
    )
    custom_id = URLField(
        CUSTOM_ID_LABLE,
        validators=[
            Length(max=CUSTOM_URL_LENGHT, message=CUSTOM_ID_VALIDATOR_LENGTH),
            Optional(),
            Regexp(REGEX, message=UNCORRECT_SYMBOLS)
        ]
    )
    submit = SubmitField(CREATE)

    def validate_custom_id(self, field):
        if field and URLMap.get(field.data):
            field.errors.append(SHORT_EXISTS)
