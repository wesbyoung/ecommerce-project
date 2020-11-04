from .import bp as blog
from flask import render_template, request, redirect, url_for, flash
from app import db
from app.models import Post, Product_Post
from flask_login import current_user, login_required

@blog.route('/create-post', methods=['POST'])
def create_post():
    if request.method == 'POST':
        r = request.form
        data = {
            'post_body': r.get('post-body'),
            'author_id': current_user.id,
        }
        p = Post(body=data['post_body'], user_id=data['author_id'])
        db.session.add(p)
        db.session.commit()
        flash("The post was created successfully", 'success')
    return redirect(url_for('index'))

@blog.route('/blog/<int:id>')
@login_required
def get_post(id):
    _id = request.args.get('id')
    post=Post.query.get(_id)
    return render_template('index.html', post=p)



@blog.route('/productpost', methods=['GET', 'POST'])
def pic_post():
    if request.method == 'POST':
        r = request.form
        data = {
            'image': r.get('image'),
            'name': r.get('name'),
            'price': r.get ('price'),
            'post_body': r.get('post-body'),
            'author_id': current_user.id,
        }
        pp = Product_Post(name=data['name'], body=data['body'], image= data['image'], price= data['price'], user_id=data['author_id'])
        db.session.add(pp)
        db.session.commit()
        flash("The post was created successfully", 'success')
    return redirect(url_for('index'))