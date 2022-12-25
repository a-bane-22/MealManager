from flask import render_template, redirect, url_for
from flask_login import login_required
from app import db
from app.models import Recipe, RecipeIngredient, Instruction
from app.helpers import get_ingredient_choices
from app.recipe import bp
from app.recipe.forms import (AddRecipeForm, AddRecipeIngredientForm,
                              AddInstructionForm)


@bp.route('/view_recipes')
@login_required
def view_recipes():
    recipes = Recipe.query.all()
    return render_template('view_recipes.html',
                           title='View Recipes',
                           recipes=recipes)


@bp.route('/view_recipe/<recipe_id>')
@login_required
def view_recipe(recipe_id):
    recipe = Recipe.query.get(int(recipe_id))
    return render_template('view_recipe.html',
                           title='View Recipe',
                           recipe=recipe)


@bp.route('/add_recipe', methods=['GET', 'POST'])
@login_required
def add_recipe():
    form = AddRecipeForm()
    if form.validate_on_submit():
        recipe = Recipe(name=form.name.data,
                        num_instructions=0)
        db.session.add(recipe)
        db.session.commit()
        return redirect(url_for('recipe.view_recipe', recipe_id=recipe.id))
    return render_template('add_recipe.html',
                           title='Add Recipe',
                           form=form)


@bp.route('/add_recipe_ingredient/<recipe_id>', methods=['GET', 'POST'])
@login_required
def add_recipe_ingredient(recipe_id):
    form = AddRecipeIngredientForm()
    form.ingredient.choices = get_ingredient_choices()
    if form.validate_on_submit():
        recipe_ingredient = RecipeIngredient(recipe_id=int(recipe_id),
                                             ingredient_id=form.ingredient.data,
                                             quantity=form.quantity.data)
        db.session.add(recipe_ingredient)
        db.session.commit()
        return redirect(url_for('recipe.view_recipe', recipe_id=recipe_id))
    return render_template('add_recipe_ingredient.html',
                           title='Add Recipe Ingredient',
                           form=form)


@bp.route('/add_instruction/<recipe_id>', methods=['GET', 'POST'])
@login_required
def add_instruction(recipe_id):
    form = AddInstructionForm()
    if form.validate_on_submit():
        recipe = Recipe.query.get(int(recipe_id))
        recipe_instruction = Instruction(recipe_id=recipe.id,
                                         instruction_number=recipe.num_instructions,
                                         instruction=form.instruction.data)
        db.session.add(recipe_instruction)
        recipe.num_instructions += 1
        db.session.add(recipe)
        db.session.commit()
        return redirect(url_for('recipe.view_recipe', recipe_id=recipe_id))
    return render_template('add_instruction.html',
                           title='Add Instruction',
                           form=form)


@bp.route('/delete_recipe/<recipe_id>')
@login_required
def delete_recipe(recipe_id):
    recipe = Recipe.query.get(int(recipe_id))
    for instruction in recipe.instructions:
        db.session.delete(instruction)
    for recipe_ingredient in recipe.ingredients:
        db.session.delete(recipe_ingredient)
    db.session.delete(recipe)
    db.session.commit()
    return redirect(url_for('recipe.view_recipes'))


@bp.route('/delete_recipe_ingredient/<ingredient_id>')
@login_required
def delete_recipe_ingredient(ingredient_id):
    recipe_ingredient = RecipeIngredient.query.get(int(ingredient_id))
    recipe_id = recipe_ingredient.recipe_id
    db.session.delete(recipe_ingredient)
    db.session.commit()
    return redirect(url_for('recipe.view_recipe', recipe_id=recipe_id))


@bp.route('/delete_instruction/<instruction_id>')
@login_required
def delete_instruction(instruction_id):
    instruction = Instruction.query.get(instruction_id)
    recipe = Recipe.query.get(instruction.recipe_id)
    db.session.delete(instruction)
    recipe.num_instructions -= 1
    db.session.add(recipe)
    db.session.commit()
    return redirect(url_for('recipe.view_recipe', recipe_id=recipe.id))
