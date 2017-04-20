from flask import render_template, request
from app import app
from .forms import QueryForm
from .search import search, search_author_from_paper, search_paper_from_author
from flask import g
import re
import sqlite3
import numpy as np
import pickle


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
            paper_authors = []
            if len(paper) == 0 or paper[0] != 'Your search did not match any paper!!!':
                for p in paper:
                    paper_authors.append(cursor.execute('select author from papers where title=' + '"' + p + '"').fetchone()[0])
            paper_authors_with_link = search_author_from_paper(cursor, paper_authors)
            print('paper authors are: ', paper_authors_with_link)
            return render_template("index.html", title='Home', form=form, paper=paper, author=author, paper_authors=paper_authors_with_link)
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
    coauthors = [a for a in coauthors if (len(a) > 1 and author != a)]

    # Find authors from the author table
    all_authors = search_author_from_paper(cursor, [author] + coauthors)
    author = all_authors[0]
    coauthors = all_authors[1:]

    # Find similar paper recommendations
    paper, author_2 = search(search_query=re.sub(r'[^\w\s]|_', '', title).lower().split(' '), search_category='p', db_cursor=cursor, num_result=4)
    recommendations = paper[1:]

    # Find the category of this paper using the pre-trained model
    # Load the pickles
    # clf pickle
    with open('text_mining/clf.pickle', 'rb') as f:
        clf = pickle.load(f)[0]

    # tfidf vectorizer pickle
    with open('text_mining/tfidf_vectorizer.pickle', 'rb') as f:
        tfidf_vectorizer = pickle.load(f)[0]

    # Transform the current title to a vector
    title_vector = tfidf_vectorizer.transform(np.array([title]))

    # Predict the category of the paper
    category = clf.predict(title_vector)

    return render_template("paper.html", title="Paper", title_=title, doi=doi, abstract=abstract,
                           author=author, coauthors=coauthors, url=url, year=year, recommendations=recommendations, category=category[0])


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

    # author_papers = get_author_papers(cursor, name)
    author_papers = search_paper_from_author(cursor, name)

    affiliations = author_row[4].split('|')
    return render_template("author.html", title=name, name=name, website=website,
                           email=email, photo=photo, affiliations=affiliations, author_papers=author_papers)
