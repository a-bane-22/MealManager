from flask import Blueprint

bp = Blueprint('recipe', __name__, template_folder='templates')

from app.recipe import routes
