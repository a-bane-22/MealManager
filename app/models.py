from werkzeug.security import check_password_hash, generate_password_hash
from app import db, login
from flask_login import UserMixin
from datetime import date
from math import floor


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(32), index=True)
    last_name = db.Column(db.String(32), index=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    phone = db.Column(db.String(10), index=True)
    password_hash = db.Column(db.String(128))
    dob = db.Column(db.Date)
    gender = db.Column(db.String(1))
    weight = db.Column(db.Float)
    height = db.Column(db.Integer)
    body_fat_percentage = db.Column(db.Integer)
    activity_level = db.Column(db.Integer)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_name(self):
        return self.first_name + ' ' + self.last_name

    def get_age_in_years(self):
        delta = date.today() - self.dob
        return floor(delta.days/365)

    def get_activity_level_description(self):
        match self.activity_level:
            case 0:
                return 'Little to No Exercise'
            case 1:
                return 'Light Exercise (1-3 days/week)'
            case 2:
                return 'Moderate Exercise (3-5 days/week)'
            case 3:
                return 'Heavy Exercise (6-7 days/week)'
            case 4:
                return 'Very Heavy Exercise (2x+/day)'
            case _:
                return 'Activity level not selected'

    def get_activity_level_multiplier(self):
        match self.activity_level:
            case 0:
                return 1.2
            case 1:
                return 1.375
            case 2:
                return 1.55
            case [3 | 4]:
                return 1.725
            case _:
                return 1

    def get_lean_body_mass_in_kg(self):
        return self.weight * (100 - self.body_fat_percentage) / 100

    # https://en.wikipedia.org/wiki/Basal_metabolic_rate
    def get_katch_mcardle_bmr(self):
        lean_body_mass = self.get_lean_body_mass_in_kg()
        return int(21.6 * lean_body_mass + 370)

    def get_katch_mcardle_daily_calories(self):
        bmr = self.get_katch_mcardle_bmr()
        activity_level_multiplier = self.get_activity_level_multiplier()
        return bmr * activity_level_multiplier

    def get_mifflin_st_jeor_bmr(self):
        bmr = int(10 * self.weight + 6.25 * self.height - 5 * self.get_age_in_years())
        match self.gender:
            case 'F':
                return bmr - 161
            case 'M':
                return bmr + 5
            case _:
                return bmr

    def get_mifflin_st_jeor_daily_calories(self):
        bmr = self.get_mifflin_st_jeor_bmr()
        activity_level_multiplier = self.get_activity_level_multiplier()
        return bmr * activity_level_multiplier


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fdc_id = db.Column(db.Integer, index=True)
    name = db.Column(db.String(32), index=True)
    calories = db.Column(db.Integer)
    fat = db.Column(db.Integer)
    protein = db.Column(db.Integer)
    carbs = db.Column(db.Integer)
    recipes = db.relationship('RecipeIngredient', backref='ingredient', lazy='dynamic')


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    num_instructions = db.Column(db.Integer)
    ingredients = db.relationship('RecipeIngredient', backref='recipe', lazy='dynamic')
    instructions = db.relationship('Instruction', backref='recipe', lazy='dynamic')

    def get_calories(self):
        calories = 0
        for recipe_ingredient in self.ingredients:
            calories += recipe_ingredient.get_calories()
        return calories

    def get_carbs(self):
        carbs = 0
        for recipe_ingredient in self.ingredients:
            carbs += recipe_ingredient.get_carbs()
        return carbs

    def get_fat(self):
        fat = 0
        for recipe_ingredient in self.ingredients:
            fat += recipe_ingredient.get_fat()
        return fat

    def get_protein(self):
        protein = 0
        for recipe_ingredient in self.ingredients:
            protein += recipe_ingredient.get_protein()
        return protein


class RecipeIngredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
    quantity = db.Column(db.Float)

    def get_ingredient_name(self):
        ingredient = Ingredient.query.get(self.ingredient_id)
        return ingredient.name

    def get_recipe_name(self):
        recipe = Recipe.query.get(self.recipe_id)
        return recipe.name

    def get_description(self):
        ingredient = Ingredient.query.get(self.ingredient_id)
        return f'{self.quantity} grams {ingredient.name}'

    def get_calories(self):
        ingredient = Ingredient.query.get(self.ingredient_id)
        return (self.quantity / 100) * ingredient.calories

    def get_carbs(self):
        ingredient = Ingredient.query.get(self.ingredient_id)
        return (self.quantity / 100) * ingredient.carbs

    def get_fat(self):
        ingredient = Ingredient.query.get(self.ingredient_id)
        return (self.quantity / 100) * ingredient.fat

    def get_protein(self):
        ingredient = Ingredient.query.get(self.ingredient_id)
        return (self.quantity / 100) * ingredient.protein


class Instruction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
    instruction_number = db.Column(db.Integer)
    instruction = db.Column(db.String(512))


class Nutrient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    unit_name = db.Column(db.String(32))
    nutrient_number = db.Column(db.Integer)
