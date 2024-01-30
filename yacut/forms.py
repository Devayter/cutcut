from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional

from yacut.constants import (CUSTOM_ID_LABLE, CUSTOM_ID_VALIDATOR_LENGTH,
                             ORIGINAL_LINK_LABLE, ORIGINAL_LINK_VALIDATOR_DATA)


class URLMapForm(FlaskForm):
    original_link = URLField(
        ORIGINAL_LINK_LABLE,
        validators=[
            DataRequired(message=ORIGINAL_LINK_VALIDATOR_DATA),
            Length(1, 256)
        ]
    )
    custom_id = URLField(
        CUSTOM_ID_LABLE,
        validators=[
            Length(1, 16, message=CUSTOM_ID_VALIDATOR_LENGTH),
            Optional()
        ]
    )
    submit = SubmitField('Создать')
