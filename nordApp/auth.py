from flask_login import login_required, login_user
from flask import (Blueprint, flash, g, redirect, render_template,request,session,url_for)
from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import LoginForm, RegistrationForm
from .models import User


bp = Blueprint('auth', __name__, url_prefix = '/auth')



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))




@bp.route('/register', methods = ['GET','POST'])
def register():

    form = RegistrationForm()

    if form.validate_on_submit():
        print('the form worked')

        # need to take in params

        name = form.name.data
        email = form.email.data
        password = form.password.data
        role = form.role.data

        error = None
        # need to query data

        # check if user already exists
        if User.query.filter_by(name = name).first() is not None:
            error = f"User {name} is already registerd."

        if error is None:

            print('Creating user')
            new_user = User(name=name,
                            email=email,
                            password=generate_password_hash(password, method="pbkdf2:sha256"),
                            role = role)
            
            # need to add and commit user
            db.session.add(new_user)
            db.session.commit()

            flash("Registration successful! Please log in.")
            return redirect(url_for('auth.login'))

        flash(error)
        print(error)

    print('form did not work: ',form.errors)

    
    return render_template('auth/register.html', form=form)


        
@bp.route('/login', methods=['POST','GET'])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        name = form.name.data
        password = form.password.data

        error = None

        user = User.query.filter_by(name=name).first()

        if user is None:
            error = "Incorrect name"
        elif not check_password_hash(user.password,password):
            error = "Incorrect username"

        if error is None:

            login_user(user)
            flash("Logged in successfully!")
            return redirect(url_for('index'))

        flash(error)

    print('form did not work: ',form.errors)

    return render_template('auth/login.html', form=form)




        # need to check if user is theree 

        

@bp.route('/logout')
def logout():
    logout_user()
    redirect(url_for('index'))