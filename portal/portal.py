from flask import Flask, render_template, flash, request
from flask import Markup
from flask_bootstrap import Bootstrap
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from timeit import default_timer as timer
import sqlite3
import numpy as np
import operator
import re


# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

# Do a db connection to sqlite, get all rows to papers variable
# papers: title, doi, abstract, author, url, year, coauthors, origin
connection = sqlite3.connect('../sqlite/paperDB.db')
cursor = connection.cursor()
cursor.execute('select * from papers')
papers = cursor.fetchall()

# get all rows from authors table
cursor.execute('select * from authors')
authors = np.array(cursor.fetchall())

class ReusableForm(Form):
    search_query = TextField('Search paper:', validators=[validators.required()])

@app.route("/", methods=['GET', 'POST'])
def index():
    form = ReusableForm(request.form)
    print(form.errors)
    if request.method == 'POST':
        search_query = re.sub(r'[^\w\s]|_', '', request.form['search_query']).lower().split(' ')
        if form.validate():
            # do search here (for now search for title)
            score_rank = []
            title_rank = []
            print('search query is: ', set(search_query))
            for index, paper in enumerate(papers):
                title = re.sub(r'[^\w\s]|_', '', paper[0]).lower().split(' ') if paper[0] is not None else ['']
                length_of_intersection = len(set(search_query).intersection(set(title)))
                l2_norm =  len(search_query) * len(title)
                cosine = (length_of_intersection / float(l2_norm)) if l2_norm != 0 else 0
                score_rank.append(cosine)
                title_rank.append(paper[0] if paper[0] is not None else '') 
            # sort the result 1st
            num_of_items = 20
            counter = 0
            rank_index = [x for (y, x) in sorted(zip(score_rank, range(len(title_rank))), reverse=True)]
            print(rank_index[1:10])
            if score_rank[rank_index[0]] == 0.0:
                flash("Your search did not match any document!!!")
            else:
                for i in rank_index:
                    if counter > num_of_items:
                        break
                    flash((str(title_rank[i]) + ' SCORE: ' + str('%.2f') % score_rank[i]))
                    flash(Markup('&nbsp;&nbsp;&nbsp;&nbsp;<a href="' + str(papers[i][4]) + '">' + str(papers[i][7]) + '</a><br>'))
                    length_of_intersection = len(set(search_query).intersection(set(title_rank[i].split(' '))))
                    l2_norm =  len(search_query) * len(title)
                    counter += 1

            # for index, title in enumerate(title_rank):
            #     if counter > num_of_items:
            #         break    
            #     flash(str(title_rank[index]) + ' SCORE: ' + str(score_rank[index]))
            #     counter += 1
        else:
            flash('All the form fields are required. ')
 
    return render_template('index.html', form=form)
 
if __name__ == "__main__":
    app.run()
