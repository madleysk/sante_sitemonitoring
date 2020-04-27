from flask import Blueprint, render_template, jsonify, request, session, redirect, flash, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from models import Users,Employe,Site
from auth import *
from forms import LoginForm,RegistrationForm
from flask_sqlalchemy import SQLAlchemy
from flask import current_app as app

auth = Blueprint('auth',__name__,template_folder='templates')
db = SQLAlchemy()

@auth.route('/subscribe',methods=['GET','POST'])
def subscribe():
	page_title = 'Inscription'
	form = RegistrationForm(request.form)
	form.auth_level.data = 1
	if request.method == 'POST' and form.validate():
		valid_data = True
		username=form.username.data
		passwd= form.passwd.data
		auth_level= form.auth_level.data
		code= form.code.data
		user_exists = Users.query.filter_by(username=username).first()
		code_exists = Users.query.filter_by(code=code).first()
		code_valid = Employe.query.filter_by(code_emp=code).first()
		if code_exists is not None:
			form.code.errors.append('Code not available !')
			valid_data = False
		if code_valid is None:
			form.code.errors.append('Code not valide !')
			valid_data = False
		if user_exists is not None:
			form.username.errors.append('Username not available !')
			valid_data = False
		if valid_data == True:
			user = Users(username=username,passwd=pass_hashing(passwd),auth_level=auth_level,code=code)
			db.session.add(user)
			db.session.commit()
			flash('Thanks for registering')
			login_user(user)
			return redirect(url_for('index'))
	return render_template('subscribe.html',page_title=page_title,form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
	page_title = 'Login'
	if current_user.is_authenticated:
		return redirect(url_for('index'))  # Bypass if user is logged in

	login_form = LoginForm(request.form)
	if request.method == 'POST' and login_form.validate():
		username = login_form.username.data
		passwd = login_form.passwd.data
		user = Users.query.filter_by(username=username).first()  # Validate Login Attempt
		if user and user.check_password(password=passwd):
		#if(pass_verify(passwd,user.passwd)):
			login_user(user)
			session['username'] = username
			session['auth_level'] = user.auth_level
			session['ucode'] = user.code
			next_page = request.args.get('next')
			return redirect(next_page or url_for('index'))
		else:
			errPWD='Erreur mot de passe.'
			flash('Invalid username/password combination')
			return render_template("login.html",page_title = 'Login',login_form=login_form,errPWD=errPWD)
	return render_template("login.html",page_title = 'Login',login_form=login_form)

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect('/')

