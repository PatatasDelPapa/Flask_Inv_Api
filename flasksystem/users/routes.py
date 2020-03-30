import enum
import jwt
import datetime
import os
from flask import render_template, url_for, flash, redirect, request, Blueprint, jsonify, make_response
from flask_login import login_user, current_user, logout_user, login_required
from flasksystem import db, bcrypt
from flasksystem.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, UpdatePasswordForm
from flasksystem.models import User
from functools import wraps

users = Blueprint('users', __name__)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        
        if not token:
            return jsonify({'message': 'No se encuentra el token!'}), 401
        
        try:
            data = jwt.decode(token, os.environ.get('SECRET_KEY'))
            usuario_actual = User.query.filter_by(id=data['id']).first()
        except:
            return jsonify({'message': 'El token es invalido!'}), 401

        return f(usuario_actual, *args, **kwargs)
        
    return decorated

@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('users.login'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data.lower(), password=hashed_password, area=form.area.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! you are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)
    

@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        print(form.password.data)
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@users.route("/logout")
def logout():
    logout_user()
    flash('You have Log out', 'info')
    return redirect(url_for('main.index'))

@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)

@users.route("/account/password", methods=['GET', 'POST'])
@login_required
def password():
    form = UpdatePasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        current_user.password = hashed_password
        db.session.commit()
        flash('Contraseña actualizada con exito', 'success')
        return redirect(url_for('users.account'))
    return render_template('password.html', form=form, legend='Cambiar contraseña')

# ---------------------------------------------------------------------------------------------


@users.route("/json/login")
def json_login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('No se pudo verificar', 401, {'WWW-Authenticate': 'Basic realm="Login Required!"'})
    
    user = User.query.filter_by(email=auth.username).first()
    
    if not user:
        return make_response('No se pudo verificar', 401, {'WWW-Authenticate': 'Basic realm="Login Required!"'})
    
    if bcrypt.check_password_hash(user.password, auth.password):
        token = jwt.encode({'id' : user.id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, os.environ.get('SECRET_KEY'))
        return jsonify({"token" : token.decode("UTF-8")})
    
    return make_response('No se pudo verificar', 401, {'WWW-Authenticate': 'Basic realm="Login Required!"'})

@users.route("/json/register", methods=['POST'])
def register():
    try:
        username = request.json['username']
        email = request.json['email']
        password = request.json['password']
        area = request.json['area']
    except:
        return jsonify({"message": "Json invalido"}), 422
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(username=username, email=email.lower(), password=hashed_password, area=area)
    db.session.add(user)
    db.session.commit()
    return user_schema.jsonify(user)

