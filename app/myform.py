from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class MyForm(FlaskForm):
    namefield = StringField('namefield', validators=[DataRequired()])
    submit = SubmitField ('Envoyer')