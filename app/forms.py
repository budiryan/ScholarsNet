from wtforms import Form, TextField, SelectField
from wtforms.validators import DataRequired


class QueryForm(Form):
    search_query = TextField('Query', validators=[DataRequired()])
    search_category = SelectField('Search for', choices=[('p', 'Paper'), ('a', 'Author'),('pa', 'Paper / Author')])
