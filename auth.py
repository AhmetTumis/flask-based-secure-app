from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db
from flask_login import login_user, login_required, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length
#from flask_limiter import Limiter
#from flask_limiter.util import get_remote_address

auth = Blueprint('auth', __name__)
#limiter = Limiter(key_func=get_remote_address)


class LoginForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired(), Length(1,6)], render_kw={"placeholder": "Username"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    remember_me = BooleanField('Keep me logged in!')
    submit = SubmitField('Log In')

@auth.route('/login')
#@limiter.limit("5 per minute")
def login():
    return render_template('login.html', form=LoginForm())

@auth.route('/login', methods=['POST'])
#@limiter.limit("5 per minute")
def login_post():

    username = ""
    password = ""
    remember = False

    form = LoginForm(request.form)
    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data
        remember = True if form.remember_me.data else False

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        flash('Wrong username or password')
        return redirect(url_for('auth.login'))
    session["username"] = username
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():

    #email = request.form.get('email')
    #username = request.form.get('username')
    #password = request.form.get('password')

    #user = User.query.filter_by(username=username).first()

    #if user:
    flash('Signing up is currently disabled please talk to your administer')
    return redirect(url_for('auth.signup'))

    #new_user = User(username=username,
    #                password=generate_password_hash(password, method='sha256'))

    #db.session.add(new_user)
    #db.session.commit()


    #return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))