from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
# from flask_socketio import SocketIO



db=SQLAlchemy()
migrate=Migrate()
login=LoginManager()
moment=Moment()


# socketio= SocketIO(app)

def create_app(config_class=Config):
    app=Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app,db)
    moment.init_app(app)

    login.init_app(app)
    login.login_view='login'
    login.login_message_category='warning'

    from app.blueprints.blog import bp as blog
    app.register_blueprint(blog)

    from app.blueprints.api import bp as api
    app.register_blueprint(api)

    from app.blueprints.shop import bp as shop
    app.register_blueprint(shop)

    

    with app.app_context():
        from .import routes, models

    return app

