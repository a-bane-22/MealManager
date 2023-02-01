from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, BooleanField, SubmitField,
                     DateField, IntegerField, FloatField, SelectField)
from wtforms.validators import InputRequired, ValidationError, Email, EqualTo
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    phone = StringField('Phone', validators=[InputRequired()])
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    password_2 = PasswordField('Repeat Password', validators=[InputRequired(), EqualTo('password')])
    dob = DateField('DOB', validators=[InputRequired()])
    gender = SelectField('Gender', validators=[InputRequired()],
                         choices=[('F', 'Female'),
                                  ('M', 'Male')])
    weight = FloatField('Weight in Kilograms', validators=[InputRequired()])
    height = IntegerField('Height in Centimeters', validators=[InputRequired()])
    body_fat_percentage = IntegerField('Body Fat Percentage', validators=[InputRequired()])
    activity_level = SelectField('Activity Level', validators=[InputRequired()],
                                 choices=[(0, 'No Regular Exercise'),
                                          (1, 'Light (1-3 days/week)'),
                                          (2, 'Moderate (3-5 days/week)'),
                                          (3, 'Heavy (6-7 days/week)'),
                                          (4, 'Very Heavy (2x+/day)')])
    submit = SubmitField('Register')

    @staticmethod
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username')

    @staticmethod
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email')
