from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.models import Post, User, Tag, db # Імпорт моделей
from app.forms import PostForm
from . import product_bp 

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
def add_post():
    form = PostForm()
    
    if form.validate_on_submit():
        
        new_post = Post(
            title=form.title.data,
            content=form.content.data,
            is_active=form.is_active.data,
            publish_date=form.publish_date.data,
            category=form.category.data,
            user_id=form.author_id.data 
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