from wtforms import Form, TextField, SelectField
from wtforms.validators import DataRequired


class QueryForm(Form):
    search_query = TextField('', validators=[DataRequired()], render_kw={"placeholder": "Your query here"})
    search_category = SelectField('Search for', choices=[('p', 'Paper'), ('a', 'Author'),('pa', 'Paper / Author')])
