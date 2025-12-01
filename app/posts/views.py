from flask import render_template, redirect, url_for, flash, session, request, abort
from sqlalchemy import select, desc
from app import db
from . import post_bp
from .models import Post
from .forms import PostForm

@post_bp.route('/create', methods=['GET', 'POST'])
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        author_name = session.get('username', 'Anonymous')
        new_post = Post(
            title=form.title.data,
            content=form.content.data,
            posted=form.publish_date.data,
            is_active=form.is_active.data,
            category=form.category.data,
            author=author_name
        )
        db.session.add(new_post)
        db.session.commit()
        flash(f"Пост '{new_post.title}' успішно додано!", 'success')
        return redirect(url_for('.list_posts'))
    return render_template('posts/add_post.html', form=form, title="Створити пост")

@post_bp.route('/')
def list_posts():
    stmt = select(Post).where(Post.is_active == True).order_by(desc(Post.posted))
    posts = db.session.scalars(stmt).all()
    return render_template('posts/list_posts.html', posts=posts)

@post_bp.route('/<int:post_id>')
def detail_post(post_id):
    post = db.get_or_404(Post, post_id)
    return render_template('posts/detail_post.html', post=post)

@post_bp.route('/<int:post_id>/update', methods=['GET', 'POST'])
def update_post(post_id):
    post = db.get_or_404(Post, post_id)
    form = PostForm(obj=post)
    if request.method == 'GET':
        form.publish_date.data = post.posted
    if form.validate_on_submit():
        form.populate_obj(post)
        db.session.commit()
        flash(f"Пост оновлено!", 'success')
        return redirect(url_for('.detail_post', post_id=post.id))
    return render_template('posts/add_post.html', form=form, title="Редагувати пост")

@post_bp.route('/<int:post_id>/delete', methods=['GET', 'POST'])
def delete_post(post_id):
    post = db.get_or_404(Post, post_id)
    if request.method == 'POST':
        db.session.delete(post)
        db.session.commit()
        flash(f"Пост видалено.", 'danger')
        return redirect(url_for('.list_posts'))
    return render_template('posts/delete_confirm.html', post=post)