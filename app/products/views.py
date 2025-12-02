import os
import secrets
from PIL import Image
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from app.models import Post, User, Tag, db
from app.forms import PostForm, RegistrationForm, LoginForm, UpdateAccountForm
from app import bcrypt
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime, timezone
from . import product_bp 

@product_bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@product_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated: 
        return redirect(url_for('bp.account'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Ваш акаунт створено! Тепер ви можете увійти.', 'success')
        return redirect(url_for('bp.login')) 
    return render_template('register.html', title='Register', form=form)

@product_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: 
        return redirect(url_for('bp.account'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.execute(db.select(User).filter_by(email=form.email.data)).scalar_one_or_none()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user) 
            flash('Вхід виконано успішно!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('bp.account'))
        else:
            flash('Вхід невдалий. Перевірте email та пароль.', 'danger')
    return render_template('login.html', title='Login', form=form)

@product_bp.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Ваш профіль оновлено!', 'success')
        return redirect(url_for('bp.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me
        
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@product_bp.route('/users_list')
@login_required
def users_list():
    users = db.session.execute(db.select(User).order_by(User.id)).scalars().all()
    user_count = len(users)
    return render_template('users_list.html', title='Users List', users=users, user_count=user_count)

@product_bp.route('/logout')
def logout():
    logout_user()
    flash('Ви вийшли із системи.', 'info')
    return redirect(url_for('bp.index')) 
    
@product_bp.route('/')
@product_bp.route('/index')
def index():
    posts = db.session.execute(
        db.select(Post)
        .order_by(Post.publish_date.desc())
        .options(db.selectinload(Post.user), db.selectinload(Post.tags))
    ).scalars().all()
    return render_template('index.html', posts=posts)

@product_bp.route('/add_post', methods=['GET', 'POST'])
@login_required
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        new_post = Post(
            title=form.title.data,
            content=form.content.data,
            is_active=form.is_active.data,
            publish_date=form.publish_date.data,
            category=form.category.data,
            user_id=current_user.id
        )
        tag_ids = form.tags.data
        if tag_ids:
             selected_tags = db.session.execute(
                db.select(Tag).where(Tag.id.in_(tag_ids))
             ).scalars().all()
             new_post.tags.extend(selected_tags)
        
        db.session.add(new_post)
        db.session.commit()
        flash(f'Post "{new_post.title}" added successfully!', 'success')
        return redirect(url_for('bp.index')) 
    return render_template('add_post.html', form=form)

@product_bp.route('/post/<int:post_id>')
def post_detail(post_id):
    post = db.session.execute(
        db.select(Post)
        .filter_by(id=post_id)
        .options(db.selectinload(Post.tags), db.selectinload(Post.user))
    ).scalar_one_or_none()
    if post is None:
        flash('Post not found!', 'danger')
        return redirect(url_for('bp.index'))
    return render_template('post_detail.html', post=post)