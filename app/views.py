from flask import render_template, request
from app import app
from .forms import QueryForm
from .search import search
import re
import sqlite3
from flask import g
from pprint import pprint


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

def get_author_papers(cursor, name):
    cursor.execute('select * from papers')
    rows = cursor.fetchall()

    all_authors = []

    for row in rows:
        authors = [row[3]]
        authors += row[6].split(', ')

        for i in range(len(authors)):
            if authors[i] != None and authors[i] != '':
                authors[i] = re.sub('\(.*\)', '', authors[i])

        abbr_authors = []
        for name in authors:
            if name == None or name == '':
                continue

            full_name = ''
            names = name.split(' ')
            for n in names[:-1]:
                if n != None and n != '':
                    full_name += n[0] + ' '
            full_name += names[-1]
            abbr_authors.append(full_name)

        all_authors.append(abbr_authors)

    papers = []

    for i in range(len(rows)):
        print(all_authors[i])
        if name in all_authors[i]:
            papers.append(rows[i][0])

    return papers


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/', methods=['GET', 'POST'])
def index():
    form = QueryForm(request.form)
    db = get_db()
    if request.method == 'POST':
        search_query = re.sub(r'[^\w\s]|_', '', request.form['search_query']).lower().split(' ')
        search_category = request.form['search_category']
        cursor = db.cursor()
        if form.validate():
            paper, author = search(search_query=search_query, search_category=search_category, db_cursor=cursor, num_result=20)
            return render_template("index.html", title='Home', form=form, paper=paper, author=author)
        else:
            print("Query cannot be empty!")
    return render_template("index.html", title='Home', form=form, paper=None, paper_index=None, author=None, author_index=None)


@app.route('/paper/<id>', methods=['GET'])
def paper(id):
    # title, doi, abstract, author, url, year, coauthors
    db = get_db()
    cursor = db.cursor()
    paper_id = str(id)
    cursor.execute('select * from papers where title=' + '"' + paper_id + '"')
    paper_row = cursor.fetchone()
    title = paper_row[0]
    doi = paper_row[1]
    abstract = paper_row[2]
    author = paper_row[3]
    url = paper_row[4]
    year = paper_row[5]
    coauthors = paper_row[6].split(',')
    # TODO: Find similar paper recommendations
    paper, author = search(search_query=re.sub(r'[^\w\s]|_', '', title).lower().split(' '), search_category='p', db_cursor=cursor, num_result=4)
    recommendations = paper[1:]
    print(recommendations)

    return render_template("paper.html", title="Paper", title_=title, doi=doi, abstract=abstract, author=author, coauthors=coauthors, url=url, year=year, recommendations=recommendations)


@app.route('/author/<id>', methods=['GET'])
def author(id):
    # name, website, email, photo, affiliations, citation_count, publication_count, publication_years, total_downloads
    db = get_db()
    cursor = db.cursor()
    author_id = str(id)
    cursor.execute('select * from authors where name=' + '"' + author_id + '"')
    author_row = cursor.fetchone()
    name = author_row[0]
    website = author_row[1]
    email = author_row[2]
    photo = author_row[3]

    author_papers = get_author_papers(cursor, name)

    affiliations = author_row[4].split('|')
    return render_template("author.html", title=name, name=name, website=website, email=email, photo=photo, affiliations=affiliations, author_papers=author_papers )
