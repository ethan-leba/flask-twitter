from flask import render_template, url_for, redirect, flash
from flask_login import login_user
from .. import db
from ..models import User
from . import auth
from .forms import LoginForm, SignupForm

@auth.route('/login', methods=['GET', 'POST'])
def login():
    loginform = LoginForm()
    signupform = SignupForm()
    if loginform.lfsubmit.data and loginform.validate_on_submit():
        successful = handle_login_request(loginform)
        if successful:
            return redirect(url_for('main.index'))
        else:
            return redirect(url_for('auth.login'))
    if signupform.sfsubmit.data and signupform.validate_on_submit():
        handle_signup_request(signupform)
        return redirect(url_for('auth.login'))
    return render_template('auth/login.html.j2', loginform=loginform, signupform=signupform)


# LoginForm -> Boolean
def handle_login_request(form):
    u = User.query.filter_by(username=form.username.data).first()
    if u is None:
        flash("User does not exist!")
    else:
        if u.verify_password(form.password.data):
            login_user(u)
            return True
        else:
            flash("Incorrect password!")
    return False

# SignupForm -> DB
def handle_signup_request(form):
    #ensures the username is unique
    print("I am reached")
    if User.query.filter_by(username=form.username.data).first() is None:
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Signed up successfully!")
    else:
        flash("That username is already taken!")
