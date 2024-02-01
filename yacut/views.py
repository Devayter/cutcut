from http import HTTPStatus

from flask import redirect, render_template, send_from_directory, url_for

from yacut.constants import OPEN_LINK
from yacut.forms import URLMapForm
from yacut.models import URLMap
from . import app


@app.route('/', methods=['GET', 'POST'], strict_slashes=False)
def index_view():
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form), HTTPStatus.OK
    try:
        url_mapping = URLMap.add_url_mapping(template='index.html', form=form)
    except ValueError:
        return render_template('index.html', form=form), HTTPStatus.OK
    if url_mapping:
        return render_template(
            'index.html',
            form=form,
            short=url_for(OPEN_LINK, short=url_mapping.short)
        ), HTTPStatus.OK
    return render_template('index.html', form=form), HTTPStatus.OK


@app.route('/<string:short>', methods=['GET'])
def open_link(short):
    return redirect(URLMap.find_original_or_404(short))


@app.route('/redoc', methods=['GET'])
def redoc_view():
    return render_template('redoc.html')


@app.route('/openapi_spec')
def openapi_spec():
    return send_from_directory(app.root_path, 'openapi.yml')
