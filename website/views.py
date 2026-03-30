from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('index.html')

@views.route('/about_me')
def about():
    return render_template('about_me.html')

@views.route('/contact')
def contact():
    return render_template('contact.html')

@views.route('/blog')
def blog():
    return render_template('blog.html')

@views.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')
