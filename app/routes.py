from .import db
from flask import current_app as app, render_template, request, redirect, url_for, flash, session
from app.models import User, Post
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
# from app.forms import MessageForm
# from app.models import Message


@app.route('/messages/<recipient>', methods=['GET', 'POST'])
@login_required
def send_message(recipient):
    user = User.query.filter_by(username=recipient).first_or_404()
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(author=current_user, recipient=user,
                      body=form.message.data)
        db.session.add(msg)
        db.session.commit()
        flash(_('Your message has been sent.'))
        return redirect(url_for('main.user', username=recipient))
    return render_template('send_message.html', title=_('Send Message'),
                           form=form, recipient=recipient)

@app.context_processor
def cart_stuff():
    if 'cart' not in session:
        session['cart'] = {
            'items': [],
            'cart_total': 0
        }
    # Reset cart total to 0 before recounting price of all items in cart
    session['cart']['cart_total'] = 0
    for i in session['cart'].get('items'):
        session['cart']['cart_total'] += i['price']
    return {'cart': session['cart']}



@app.route('/')
@login_required
def index():
    # print("Current User:", current_user)
    # print("Active User:", current_user.is_active)
    # print("Anonymous User:", current_user.is_anonymous)
    # print("Authenticated User:", current_user.is_authenticated)
    # print("ID of User:", current_user.get_id())
    if current_user.is_authenticated:
        posts= current_user.followed_posts().all()
        # posts= Post.query.order_by(Post.created_on.desc()).all()
        # posts = Post.query.filter_by(user_id=current_user.id).order_by(Post.created_on.desc()).all()
    else: 
        posts = []
    context = {
        'posts': posts
    }
    return render_template('index.html', posts=posts)

@app.route('/messages')
@login_required
def messages():
    return render_template('messages.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        r = request.form
        if r.get('confirm_password') == r.get('password'):
            data = {
                'first_name': r.get('first_name'),
                'last_name': r.get('last_name'),
                'email': r.get('email'),
                'password': r.get('password'),
            }
            u = User(first_name=data['first_name'], last_name=data['last_name'], email=data['email'], password=data['password'])
            u.hash_password(u.password)
            db.session.add(u)
            db.session.commit()
            flash("You have registered successfully", 'primary')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        r = request.form
        user = User.query.filter_by(email=r.get('email')).first()
        if user is None or not user.check_password(r.get('password')):
            flash("You have used either an incorrect email or password", 'danger')
            return redirect(url_for('login'))
        login_user(user, remember=r.get('remember_me'))
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
            return redirect(next_page)
        flash("You have logged in successfully", 'success')
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    flash("You have successfully logged out", 'info')
    return redirect(url_for('login'))

@app.route('/profile')
def profile():
    user = {
        'id': current_user.id,
        'first_name':current_user.first_name,
        'last_name':current_user.last_name,
        'email':current_user.email
    }

    context = {
        'user': user,
        'posts': current_user.posts,
        'users': [user for user in User.query.all() if current_user !=user]  
    }
    return render_template('profile.html', **context)




@app.route('/users/follow')
def follow():
     _id = request.args.get('id')
     user = User.query.get(_id)
     current_user.follow(user)
     db.session.commit()
     flash(f'You are now following {user.first_name}  {user.last_name}', 'success')
     return redirect(url_for('profile'))
    


@app.route('/users/unfollow')
def unfollow():
     _id = request.args.get('id')
     user = User.query.get(_id)
     current_user.unfollow(user)
     db.session.commit()
     flash(f'You have unfollowed {user.first_name}  {user.last_name}',  'danger')
     return redirect(url_for('profile'))
    

