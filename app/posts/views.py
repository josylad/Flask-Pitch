from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from app import db
from app.models import Post, User, Comment
from app.posts.forms import PostForm, CommentForm

posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user, category=form.category.data)
        db.session.add(post)
        db.session.commit()
        flash('You pitch has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('new-post.html', title='New Pitch', form=form, legend='New Pitch')


@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_id = post_id).all()
    return render_template('post.html', title=post.title, post=post, comments = comments)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your pitch has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('new-post.html', title='Update Post', form=form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your pitch has been deleted!', 'success')
    return redirect(url_for('main.home'))


@posts.route("/post/<string:category>")
def category_post(category):
    
    post = Post.query.filter_by(category=category).all()
    print("..............", post)
    return render_template('category.html', post=post, category=category) 


@posts.route("/post/<int:post_id>/comment", methods=['GET', 'POST'])
@login_required
def new_comment(post_id):
    post = Post.query.get_or_404(post_id)
    
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(comment=form.comment.data, author=current_user, post_id = post_id )
        db.session.add(comment)
        db.session.commit()
        # comments = Comment.query.all()
        flash('You comment has been created!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    return render_template('new-comment.html', title='New Comment', form=form, legend='New Comment')

