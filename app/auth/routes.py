from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import check_password_hash
auth = Blueprint('auth', __name__, template_folder='auth_templates')
from flask_login import current_user, login_user, logout_user
from ..forms import SignUpForm, LoginForm
from ..models import User


@auth.route('/login', methods=['GET', 'POST'])
def loginPage():
    form = LoginForm()
    if request.method == "POST":
        if form.validate():
          username = form.username.data
          password = form.password.data
          print(username, password)
        user = User.query.filter_by(username=username).first()
        if user:
            print(user)
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect (url_for('homePage'))             
            else:
                flash('nope!')
        else:
            flash('nope!',category='danger')
    return render_template('login.html', form = form)

@auth.route('/register', methods=['GET', 'POST'])
def registerPage():
    form = SignUpForm()
    if request.method == "POST":
        if form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data
            if User.query.filter_by(username=username).first():
                flash('That username already exists, please try another!', 'warning')
                return redirect(url_for('auth.RegisterPage'))
            if User.query.filter_by(email=email).first():
                flash('that email has been used previously, try again', 'warning')
                return redirect(url_for('auth.loginPage'))
            user = User(username, email, password)
            user.saveUser()
            return redirect (url_for('auth.loginPage'))
    return render_template('register.html', form=form)


@auth.route('/logout')
def logOut():
    logout_user()
    return redirect (url_for('homePage'))