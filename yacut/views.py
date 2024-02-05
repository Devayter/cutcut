from http import HTTPStatus

from flask import (
    abort, flash, redirect, render_template, send_from_directory, url_for
)
from yacut.constants import SHORT_ROUTE
from yacut.forms import URLMapForm
from yacut.models import URLMap
from . import app

SHORT_DOES_NOT_EXIST = 'Короткая ссылка {short} не существует'


@app.route('/', methods=['GET', 'POST'], strict_slashes=False)
def index_view():
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form), HTTPStatus.OK
    try:
        return render_template(
            'index.html',
            form=form,
            short=url_for(
                SHORT_ROUTE,
                short=URLMap.add(
                    form.original_link.data,
                    form.custom_id.data if form.custom_id.data else None
                ).short,
                _external=True
            )
        ), HTTPStatus.OK
    except ValueError:
        return render_template('index.html', form=form), HTTPStatus.OK
    except RuntimeError as error:
        flash(str(error))
        return (
            render_template('index.html', form=form),
            HTTPStatus.INTERNAL_SERVER_ERROR
        )


@app.route('/<string:short>', methods=['GET'])
def open_link(short):
    url_mapping = URLMap.get(short)
    if not url_mapping:
        abort(HTTPStatus.NOT_FOUND)
    return redirect(url_mapping.original)


@app.route('/redoc', methods=['GET'])
def redoc_view():
    return render_template('redoc.html')


@app.route('/openapi_spec')
def openapi_spec():
    return send_from_directory(app.root_path, 'openapi.yml')
