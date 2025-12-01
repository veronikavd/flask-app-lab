from . import post_bp
from flask import request, render_template, abort, flash, redirect, url_for
from app.posts.forms import PostForm
from app import db  
from app.posts.models import Post  

@post_bp.route('/')
def get_posts():
    posts = Post.query.order_by(Post.posted.desc()).all()
    return render_template("posts.html", posts=posts)


@post_bp.route('/<int:id>')
def detail_post(id):
    post = Post.query.get_or_404(id)  
    return render_template("detail_post.html", post=post)


@post_bp.route('/add_post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        new_post = Post(
            title=form.title.data,
            content=form.content.data,
            author="Admin"  
        )
        db.session.add(new_post)
        db.session.commit()  
        flash('Post added successfully!', 'success')
        return redirect(url_for('posts.get_posts'))
    return render_template('add_post.html', form=form)


@post_bp.route('/delete/<int:id>', methods=['GET','POST'])
def delete_post(id):
    post = Post.query.get_or_404(id)  
    db.session.delete(post)  
    db.session.commit()  

    flash('Post has been deleted successfully!', 'success') 
    return redirect(url_for('posts.get_posts'))  

@post_bp.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)  
    form = PostForm(obj=post)  

    if form.validate_on_submit():  
        post.title = form.title.data
        post.content = form.content.data
        post.author = form.author.data  
        post.category = form.category.data  
        post.posted = form.publish_date.data  

        db.session.commit()  
        flash('Post updated successfully!', 'success')  
        return redirect(url_for('posts.get_posts'))  
    return render_template('edit_post.html', form=form, post=post)  

@post_bp.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
