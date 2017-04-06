from flask import render_template
from app import app
from .forms import QueryForm


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = QueryForm()
    if form.validate_on_submit():
        pass
    return render_template("index.html", title='Home', form=form)
