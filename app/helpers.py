from app.models import Ingredient


# Pre:  Ingredient is a table model with columns id and name and the
#        corresponding table has been created
# Post: RV = a list of tuples containing the id and name of each ingredient
#            in the table
def get_ingredient_choices():
    ingredients = Ingredient.query.all()
    choices = [(ingredient.id, ingredient.name) for ingredient in ingredients]
    return choices
