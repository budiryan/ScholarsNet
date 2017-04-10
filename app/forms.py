from wtforms import Form, TextField, SelectField
from wtforms.validators import DataRequired


class QueryForm(Form):
    search_query = TextField('', validators=[DataRequired()], render_kw={"placeholder": "Your query here"})
    search_category = SelectField('Search for', choices=[('pa', 'Paper / Author'), ('p', 'Paper'), ('a', 'Author')])
