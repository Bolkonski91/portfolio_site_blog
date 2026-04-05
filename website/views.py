from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from website import db
from .models import ContactMessage

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('index.html')

@views.route('/about_me')
def about():
    return render_template('about_me.html')

@views.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        email = request.form['email']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        title = request.form['title']
        message = request.form['message']
        if len(email) < 8:
            flash('Please enter a valid email address.')
        elif len(title) < 1:
            flash('Please enter title of message, it is required field.')
        elif len(message) < 10:
            flash('This field can\'t be empty and must have minimum 10 character\'s , it is required field.')
        else:
            new_message = ContactMessage(
                email = email,
                first_name = first_name,
                last_name = last_name,
                title = title,
                message = message,
            )
            db.session.add(new_message)
            db.session.commit()
            flash('Your message is successfully send, and I\'ll answer soon.', category='success')
            return redirect(url_for('views.contact'))
    return render_template('contact.html')

@views.route('admin/messages')
def messages():
    all_messages = ContactMessage.query.order_by(ContactMessage.date_sent.desc()).all()
    return render_template('messages.html', messages=all_messages)

@views.route('/blog')
def blog():
    return render_template('blog.html')

@views.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

@views.route('/admin')
@login_required
def admin():
    return render_template('admin.html', user=current_user)