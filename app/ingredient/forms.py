from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, IntegerField)
from wtforms.validators import InputRequired


class AddIngredientForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    calories = IntegerField('Calories', validators=[InputRequired()])
    fat = IntegerField('Fat', validators=[InputRequired()])
    protein = IntegerField('Protein', validators=[InputRequired()])
    carbs = IntegerField('Carbs', validators=[InputRequired()])
    submit = SubmitField('Submit')
