from flask import Blueprint

auth = Blueprint('auth', __name__)

auth.route('/login', methods=['GET', 'POST'])
def login():
    pass

auth.route('/logout', methods=['GET', 'POST'])
def logout():
    pass

auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    pass