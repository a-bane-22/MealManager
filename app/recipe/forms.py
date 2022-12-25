from flask_wtf import FlaskForm
from wtforms import (IntegerField, StringField, SelectField, SubmitField)
from wtforms.validators import InputRequired
from app.helpers import get_ingredient_choices


class AddRecipeForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    submit = SubmitField('Submit')


class AddRecipeIngredientForm(FlaskForm):
    ingredient = SelectField('Ingredient', validators=[InputRequired()])
    quantity = IntegerField('Quantity (g)', validators=[InputRequired()])
    submit = SubmitField('Submit')


class AddInstructionForm(FlaskForm):
    instruction = StringField('Instruction', validators=[InputRequired()])
    submit = SubmitField('Submit')
