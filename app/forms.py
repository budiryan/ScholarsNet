from flask_wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired


class QueryForm(Form):
    search_query = StringField('Query', validators=[DataRequired()])
    paper = BooleanField('Papers', default=False)
    author = BooleanField('Authors', default=False)
