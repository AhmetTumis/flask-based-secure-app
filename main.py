from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user
from .models import User
from . import db, models
from wtforms import StringField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import Length
#from flask_limiter import Limiter
#from flask_limiter.util import get_remote_address

main = Blueprint('main', __name__)
#limiter = Limiter(key_func=get_remote_address)


class ProfileForm(FlaskForm):
    address = StringField('Address', validators=[Length(0,100)],render_kw={"placeholder": "Address"})
    email = StringField('Email', validators=[Length(0,100)],render_kw={"placeholder": "test"})
    phonenumber = StringField('Phonenumber', validators=[Length(0,12)],render_kw={"placeholder": "test"})
    feedback = StringField('Feedback', validators=[Length(0,1000)],render_kw={"placeholder": "test"})
    submit = SubmitField('Submit')

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.username, form=ProfileForm())

@main.route('/profile', methods=['POST'])
@login_required
def profile_post():

    #gelen boş mu diye bak
    user = User.query.filter_by(username=current_user.username).first()
    form = ProfileForm(request.form)

    if form.validate_on_submit():
        address = form.address.data
        email = form.email.data
        phonenumber = form.phonenumber.data
        feedback = form.feedback.data

        if address != '':
            user.address = address
        if email != '':
            user.email = email
        if phonenumber != '':
            user.phone = phonenumber
        if feedback != '':
            user.feedback = feedback

        db.session.commit()

        return render_template('profile.html', name="the update was a success!", form=ProfileForm())

    return render_template('profile.html', name="there was a problem!", form=ProfileForm())

@main.route('/data')
@login_required
def profile_data():

    user = User.query.filter_by(username=current_user.username).first()
    user_data = {
        'username': user.username,
        'address':  user.address,
        'email': user.email,
        'phone': user.phone,
        'feedback': user.feedback
    }

    return render_template('profiledata.html', user=user_data)