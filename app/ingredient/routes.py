from flask import render_template, redirect, url_for
from flask_login import login_required
from app import db
from app.models import Ingredient
from app.ingredient import bp
from app.ingredient.forms import AddIngredientForm


@bp.route('/view_ingredients')
@login_required
def view_ingredients():
    ingredients = Ingredient.query.all()
    return render_template('view_ingredients.html',
                           title='View Ingredients',
                           ingredients=ingredients)


@bp.route('/view_ingredient/<ingredient_id>')
@login_required
def view_ingredient(ingredient_id):
    ingredient = Ingredient.query.get(int(ingredient_id))
    return render_template('view_ingredient.html',
                           title='View Ingredient',
                           ingredient=ingredient)


@bp.route('/add_ingredient', methods=['GET', 'POST'])
@login_required
def add_ingredient():
    form = AddIngredientForm()
    if form.validate_on_submit():
        ingredient = Ingredient(name=form.name.data,
                                calories=form.calories.data,
                                fat=form.fat.data,
                                protein=form.protein.data,
                                carbs=form.carbs.data)
        db.session.add(ingredient)
        db.session.commit()
        return redirect(url_for('ingredient.view_ingredient', ingredient_id=ingredient.id))
    return render_template('add_ingredient.html', title='Add Ingredient', form=form)
