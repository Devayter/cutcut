from http import HTTPStatus

from flask import jsonify, request

from yacut.constants import (CUSTOM_LENGHT, NO_DATA, NO_URL, UNCORRECT_ID,
                             UNCORRECT_NAME, URL_EXISTS, URL_FOR_API)
from yacut.error_handlers import InvalidAPIUsage
from yacut.models import URLMap
from yacut.views import check_short, get_short
from . import app, db


@app.route('/api/id/', methods=['POST'])
def add_url():
    data = request.get_json()
    url = URLMap()
    if not data:
        raise InvalidAPIUsage(NO_DATA)
    if 'url' not in data:
        raise InvalidAPIUsage(NO_URL)
    if 'custom_id' in data and data['custom_id']:
        if URLMap.query.filter_by(short=data['custom_id']).first():
            raise InvalidAPIUsage(URL_EXISTS)
        if (len(data['custom_id']) > CUSTOM_LENGHT
                or not check_short(data['custom_id'])):
            raise InvalidAPIUsage(UNCORRECT_NAME)
    short = get_short() if not data.get('custom_id') else data.get('custom_id')
    url = URLMap(
        original=data['url'],
        short=short
    )
    db.session.add(url)
    db.session.commit()
    print()
    return jsonify(
        {'url': url.original,
         'short_link': URL_FOR_API.format(short=url.short)}
    ), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_url(short_id):
    url = URLMap.query.filter_by(short=short_id).first()
    if not url:
        raise InvalidAPIUsage(UNCORRECT_ID, HTTPStatus.NOT_FOUND)
    return jsonify({'url': url.original})
