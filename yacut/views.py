from http import HTTPStatus

from flask import flash, redirect, render_template

from yacut.constants import UNCORRECT_NAME, URL_EXISTS, URL_SUCCESS_CREATED
from yacut.forms import URLMapForm
from yacut.models import URLMap
from yacut.utils import check_short, get_short
from . import app, db


@app.route('/', methods=['GET', 'POST'], strict_slashes=False)
def index_view():
    form = URLMapForm()
    if form.validate_on_submit():
        original = form.original_link.data
        short = form.custom_id.data if form.custom_id.data else get_short()
        if URLMap.query.filter_by(short=short).first():
            flash(URL_EXISTS)
            return render_template('index.html', form=form)
        if not check_short(short):
            flash(UNCORRECT_NAME)
            return render_template('index.html', form=form)
        url = URLMap(
            original=original,
            short=short
        )
        db.session.add(url)
        db.session.commit()
        flash(URL_SUCCESS_CREATED.format(short=short))
    return render_template('index.html', form=form), HTTPStatus.OK


@app.route('/<string:short>', methods=['GET'])
def open_link(short):
    return redirect(
        URLMap.query.filter_by(short=short).first_or_404().original
    )
