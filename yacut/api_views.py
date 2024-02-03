from http import HTTPStatus

from flask import jsonify, request, url_for

from yacut.constants import SHORT_ROUTE
from yacut.error_handlers import InvalidAPIUsage
from yacut.models import URLMap
from . import app

NO_DATA = 'Отсутствует тело запроса'
NO_URL = '"url" является обязательным полем!'
SHORT_LINK = 'http://localhost{short}'
UNCORRECT_ID = 'Указанный id не найден'


@app.route('/api/id/', methods=['POST'])
def add_url():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage(NO_DATA)
    if 'url' not in data:
        raise InvalidAPIUsage(NO_URL)
    try:
        short = URLMap.add_url_mapping(
            data['url'],
            (data['custom_id'] if 'custom_id' in data and data['custom_id']
             else URLMap.generate_short())
        ).short
    except ValueError as error:
        raise InvalidAPIUsage(str(error), status_code=HTTPStatus.BAD_REQUEST)
    return jsonify(
        {ç
            'url': data['url'],
            'short_link': url_for(
                SHORT_ROUTE, short=short, _external=True
            )
        }
    ), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_url(short_id):
    try:
        return jsonify({'url': URLMap.get(short_id).original})
    except AttributeError:
        raise InvalidAPIUsage(UNCORRECT_ID, status_code=HTTPStatus.NOT_FOUND)
