from werkzeug.security import check_password_hash, generate_password_hash
from app import db, login
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(32), index=True)
    last_name = db.Column(db.String(32), index=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    phone = db.Column(db.String(10), index=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_name(self):
        return self.first_name + ' ' + self.last_name


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
