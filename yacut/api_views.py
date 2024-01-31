from http import HTTPStatus

from flask import jsonify, request, url_for

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
    url_mapping = URLMap.add_url_mapping_for_api(data)
    return jsonify(
        {'url': url_mapping.original,
         'short_link': SHORT_LINK.format(
             short=url_for('open_link', short=url_mapping.short)
         )}
    ), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_url(short_id):
    url_mapping = URLMap.find_original_for_api(short_id)
    return jsonify({'url': url_mapping.original})
