from flask import Blueprint, render_template, request, url_for, redirect, flash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    data = request.form
    print(data)
    return render_template('login.html', text='texting')

@auth.route('/logout')
def logout():
    pass

@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form['email']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        password1 = request.form['password1']
        password2 = request.form['password2']
        username = request.form['username']
        if password1 != password2:
            flash('Passwords do not match', category='error')
        elif len(email) < 6:
            flash('Email must be at least 6 characters', category='error')
        elif len(firstName) < 2:
            flash('First name must be at least 2 characters', category='error')
        elif len(lastName) < 2:
            flash('Last name must be at least 2 characters', category='error')
        elif len(username) < 2:
            flash('Username must be at least 2 characters', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters', category='error')
        else:
            flash('Account created successfully!', category='success')

    return render_template('sign_up.html')