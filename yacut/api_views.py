from http import HTTPStatus
from urllib.parse import urljoin

from flask import jsonify, request, url_for

from yacut.constants import OPEN_LINK
from yacut.error_handlers import InvalidAPIUsage
from yacut.models import URLMap
from . import app

NO_DATA = 'Отсутствует тело запроса'
NO_URL = '"url" является обязательным полем!'
SHORT_LINK = 'http://localhost{short}'


@app.route('/api/id/', methods=['POST'])
def add_url():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage(NO_DATA)
    if 'url' not in data:
        raise InvalidAPIUsage(NO_URL)
    try:
        url_mapping = URLMap.add_url_mapping(data=data)
    except ValueError as error:
        return jsonify({'message': str(error)}), HTTPStatus.BAD_REQUEST
    return jsonify(
        {
            'url': url_mapping.original,
            'short_link': urljoin(
                request.url_root, url_for(OPEN_LINK, short=url_mapping.short)
            )
        }
    ), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_url(short_id):
    try:
        url_mapping = URLMap.find_url_mapping(short_id)
    except ValueError as error:
        return jsonify({'message': str(error)}), HTTPStatus.NOT_FOUND
    return jsonify({'url': url_mapping.original})
