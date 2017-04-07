from wtforms import Form, TextField, BooleanField
from wtforms.validators import DataRequired


class QueryForm(Form):
    search_query = TextField('Query', validators=[DataRequired()])
    paper = BooleanField('Papers', default=False)
    author = BooleanField('Authors', default=False)
