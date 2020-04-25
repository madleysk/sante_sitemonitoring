from flask import Blueprint, render_template, jsonify, request, session, redirect, flash, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from models import Users
from forms import LoginForm

auth = Blueprint('auth',__name__,template_folder='templates')

@auth.route('/subscribe',methods=['GET','POST'])
def subscribe():
	page_title = 'Inscription'
	form = RegistrationForm(request.form)
	if request.method == 'POST' and form.validate():
		user = Users(form.username.data,form.email.data,form.password.data)
		flash('Thanks for registering')
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
