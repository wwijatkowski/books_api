from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SearchField(FlaskForm):
    title = StringField('Title:', validators=[DataRequired()], default="Hobbit")
    submit = SubmitField('Search')

