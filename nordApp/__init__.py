import os

from flask import Flask, render_template
import secrets
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect



db = SQLAlchemy()
login_manager = LoginManager()



def create_app(test_config=None):


    app = Flask(__name__, instance_relative_config=True)

    app.config['SECRET_KEY'] = secrets.token_hex(16)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nordManager.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        

    login_manager.init_app(app)
    bootstrap = Bootstrap(app)
    db.init_app(app)
    csrf = CSRFProtect(app)

    
    #import models to initialize database
    from .models import User, Shift

    #Create tables
    with app.app_context():
        db.create_all()



    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass



    @app.route('/')
    def index():
        return render_template('index.html')

    from .auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from .schedule import bp as schedule_bp
    app.register_blueprint(schedule_bp)


    





    return app