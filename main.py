from flask import Flask, Blueprint, render_template, request, flash, redirect, url_for
from models import User
from __init__ import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user


# load by auth.login
auth = Blueprint('auth', __name__)

# login page
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # get variable from text box
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='succes')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Wrong password, please try again.', category='error')
        else:
            flash("This username does not exist")

    return render_template("index.html", user=current_user)


# log out option
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


# register page
@auth.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        # take variable from user
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(username=username).first()
        if user:
            flash('This username is already using.', category='error')
        elif len(username) < 2:
            flash('Username must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords do not match.', category='error')
        elif len(password1) < 3:
            flash('Password must be at least 3 characters', category='error')
        else:
            # save new user in database.db by User class from models.py
            new_user = User(username=username, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Your player is ready!')
            return redirect(url_for('views.home'))

    return render_template('register.html', user=current_user)





