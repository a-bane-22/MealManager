from flask import Blueprint

bp = Blueprint('ingredient', __name__, template_folder='templates')

from app.ingredient import routes