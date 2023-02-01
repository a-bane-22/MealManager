from flask import render_template, flash, redirect, url_for
from flask_login import current_user, logout_user, login_required
from werkzeug.utils import secure_filename
from app import db
from app.models import User
from app.main import bp
from app.main.forms import EditUserForm
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


@bp.route('/edit_user/<user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    user = User.query.get(int(user_id))
    form = EditUserForm()
    if form.validate_on_submit():
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.email = form.email.data
        user.phone = form.phone.data
        user.dob = form.dob.data
        user.gender = form.gender.data
        user.weight = form.weight.data
        user.height = form.height.data
        user.body_fat_percentage = form.body_fat_percentage.data
        user.activity_level = form.activity_level.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('main.view_user', user_id=user.id))
    form.first_name.data = user.first_name
    form.last_name.data = user.last_name
    form.email.data = user.email
    form.phone.data = user.phone
    form.dob.data = user.dob
    form.gender.data = user.gender
    form.weight.data = user.weight
    form.height.data = user.height
    form.body_fat_percentage.data = user.body_fat_percentage
    form.activity_level.data = user.activity_level
    return render_template('edit_user.html', title='Edit User', form=form)