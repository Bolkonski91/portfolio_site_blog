from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from website import db
from .models import ContactMessage, Blog

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
            flash('Please enter a valid email address, it is required field.', category='error')
        elif len(title) < 1:
            flash('Please enter title of message, it is required field.', category='error')
        elif len(message) < 10:
            flash('This field can\'t be empty and must have minimum 10 character\'s, it is required field.', category='error')
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

@views.route('/admin/messages')
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
    user_blogs = Blog.query.filter_by(user_id=current_user.id).order_by(Blog.date_posted.desc()).all()
    return render_template('admin.html', user=current_user, posts=user_blogs)

@views.route('/admin/add_post', methods=['GET', 'POST'])
@login_required
def add_post():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['content']
        summary = request.form.get('summary', '')

        if len(title) < 3:
            flash('Naslov mora imati najmanje 3 karaktera!', category='error')
        elif len(text) < 10:
            flash('Sadržaj mora imati najmanje 10 karaktera!', category='error')
        else:
            # Kreiraj novi Blog post
            new_blog = Blog(
                title=title,
                text=text,
                user_id=current_user.id
            )
            db.session.add(new_blog)
            db.session.commit()
            flash('Post je uspešno kreiran!', category='success')
            return redirect(url_for('views.admin'))

    return render_template('add_post.html')


@views.route('/admin/post/<int:post_id>', methods=['GET'])
@login_required
def view_post(post_id):
    post = Blog.query.get_or_404(post_id)
    # Provera da li je vlasnik posta
    if post.user_id != current_user.id:
        flash('Nemate pristup ovom postu!', category='error')
        return redirect(url_for('views.admin'))
    return render_template('view_post.html', post=post)


@views.route('/admin/post/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Blog.query.get_or_404(post_id)
    if post.user_id != current_user.id:
        flash('Nemate pristup ovom postu!', category='error')
        return redirect(url_for('views.admin'))

    if request.method == 'POST':
        post.title = request.form['title']
        post.text = request.form['content']
        db.session.commit()
        flash('Post je uspešno ažuriran!', category='success')
        return redirect(url_for('views.admin'))

    return render_template('edit_post.html', post=post)


@views.route('/admin/post/delete/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Blog.query.get_or_404(post_id)
    if post.user_id != current_user.id:
        flash('Nemate pristup ovom postu!', category='error')
        return redirect(url_for('views.admin'))

    db.session.delete(post)
    db.session.commit()
    flash('Post je uspešno obrisan!', category='success')
    return redirect(url_for('views.admin'))