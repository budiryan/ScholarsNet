from flask import render_template, request
from app import app
from .forms import QueryForm
from .search import search
import re


@app.route('/', methods=['GET', 'POST'])
def index():
    form = QueryForm(request.form)
    if request.method == 'POST':
        search_query = re.sub(r'[^\w\s]|_', '', request.form['search_query']).lower().split(' ')
        paper_checkbox = request.form.get('paper')
        author_checkbox = request.form.get('author')
        if form.validate():
            print(search(query=search_query, paper=paper_checkbox, author=author_checkbox))
    return render_template("index.html", title='Home', form=form)
