from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired


class QueryForm(Form):
    search_query = StringField('Search', validators=[DataRequired()])
