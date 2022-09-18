from flask import render_template, flash, redirect, url_for
from flask_login import current_user, logout_user, login_required
from werkzeug.utils import secure_filename
from app import db
from app.models import User
from app.main import bp
from datetime import date
import os


@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html', title='Home')


@bp.route('/view_users')
@login_required
def view_users():
    users = User.query.all()
    return render_template('view_users.html', title='Users', users=users)


@bp.route('/view_user/<user_id>')
@login_required
def view_user(user_id):
    user = User.query.get(int(user_id))
    return render_template('view_user.html', title='User Dashboard', user=user)
