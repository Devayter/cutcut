from http import HTTPStatus

from flask import redirect, render_template, url_for

from yacut.forms import URLMapForm
from yacut.models import URLMap

from . import app

URL_SUCCESS_CREATED = 'Ваша новая ссылка готова: http://localhost{short}'


@app.route('/', methods=['GET', 'POST'], strict_slashes=False)
def index_view():
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form), HTTPStatus.OK
    url_mapping = URLMap.add_url_mapping('index.html', form)
    if url_mapping:
        return render_template(
            'index.html',
            form=form,
            short_url_message=URL_SUCCESS_CREATED.format(
                short=url_for('open_link', short=url_mapping.short)
            )
        ), HTTPStatus.OK
    return render_template('index.html', form=form), HTTPStatus.OK


@app.route('/<string:short>', methods=['GET'])
def open_link(short):
    return redirect(URLMap.find_original(short))
