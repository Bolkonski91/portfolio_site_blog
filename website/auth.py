from flask import Blueprint, render_template

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html', text='texting')

@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    pass

@auth.route('/sign_up')
def sign_up():
    return render_template('sign_up.html')