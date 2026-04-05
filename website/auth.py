from flask import Blueprint, render_template, request, url_for, redirect, flash
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from website import db
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                flash('Login Successful.', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.admin'))
            else:
                flash('Login Unsuccessful,', category='error')
        else:
            flash('Email isn\'t registered.', category='error')

    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form['email']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        password1 = request.form['password1']
        password2 = request.form['password2']
        username = request.form['username']

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already registered.', category='error')
        elif password1 != password2:
            flash('Passwords do not match', category='error')
        elif len(email) < 6:
            flash('Email must be at least 6 characters', category='error')
        elif len(username) < 2:
            flash('Username must be at least 2 characters', category='error')
        elif len(firstName) < 2:
            flash('First name must be at least 2 characters', category='error')
        elif len(lastName) < 2:
            flash('Last name must be at least 2 characters', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters', category='error')
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(password1, method='pbkdf2:sha256', salt_length=16), firstName=firstName, lastName=lastName)
            db.session.add(new_user)
            db.session.commit()

            flash('Account created successfully!', category='success')
            return redirect(url_for('views.home'))

    return render_template('sign_up.html', user=current_user)