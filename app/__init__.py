from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from app.config import Config
from flask_migrate import Migrate
from app.config import config_options
from flask_mail import Mail


login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'


app = Flask(__name__)
mail = Mail()
db = SQLAlchemy()
bcrypt = Bcrypt()



def create_app(config_class=Config):
    
    # Creating the app configurations
    app.config.from_object(__name__)
    
    app.config['SECRET_KEY'] = '6647hdhe779ndmnd9383nj2u'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://josylad:p@localhost/pitchy'
    app.config['DEBUG']=True
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    
    from app.users.views import users 
    from app.posts.views import posts
    from app.main.views import main 
    
    
    return app