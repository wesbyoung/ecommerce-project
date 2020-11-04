from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Message {}>'.format(self.body)

class Product_Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String)
    image= db.Column(db.String)
    price= db.Column(db.Float)
    title = db.Column(db.String)
    body = db.Column(db.Text)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    updated_on = db.Column(db.DateTime)
    user_id = db.Column(db.ForeignKey('user.id'))
    

    def __repr__(self):
        return f"<Post: {self.body[:20]}"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    body = db.Column(db.Text)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    updated_on = db.Column(db.DateTime)
    user_id = db.Column(db.ForeignKey('user.id'))

    def __repr__(self):
        return f"<Post: {self.body[:20]}..."

    def to_dict(self):
        data = {
            'id': self.id,
            'body': self.body,
            'created_on': self.created_on,
            'updated_on': self.updated_on,
            'user': {
                'id': self.user_id,
                'first_name': User.query.get(self.user_id).first_name,
                'last_name': User.query.get(self.user_id).last_name,
                'email': User.query.get(self.user_id).email
            }
        }


followers=db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
    )

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Post', backref='user', lazy=True)
    messages_sent = db.relationship('Message',foreign_keys='Message.sender_id',backref='author', lazy='dynamic')
    messages_received = db.relationship('Message', foreign_keys='Message.recipient_id',backref='recipient', lazy='dynamic')
    last_message_read_time = db.Column(db.DateTime)
    followed = db.relationship(
        'User', 
        secondary = followers,
        primaryjoin=(followers.c.follower_id==id),
        secondaryjoin=(followers.c.followed_id==id),
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic'
    )

    def new_messages(self):
        last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
        return Message.query.filter_by(recipient=self).filter(Message.timestamp > last_read_time).count()

    def followed_posts(self):
            followed_posts=Post.query.join(followers,(followers.c.followed_id==Post.user_id)).filter(followers.c.follower_id==self.id).order_by(Post.created_on.desc())
            my_posts=Post.query.filter_by(user_id=self.id)
            return followed_posts.union(my_posts).order_by(Post.created_on.desc())

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

        
    def unfollow(self, user):
         if self.is_following(user):
            self.followed.remove(user)
        
    def is_following(self, user):
         return self.followed.filter(followers.c.followed_id==user.id).count()>0
    
        

    def hash_password(self, original_password):
        self.password = generate_password_hash(original_password)

    def check_password(self, original_password):
        return check_password_hash(self.password, original_password)

    def __repr__(self):
        return f"<User: {self.email}>"

@login.user_loader
def login_user(id):
    return User.query.get(int(id))