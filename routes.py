from flask import Blueprint, render_template
from flask_login import current_user, login_required
from flask import current_app as app
#from .assets import compile_auth_assets

main_bp = Blueprint('main_bp',__name__,template_folder='templates',static_folder='static')
#compile_auth_assets(app)

@main_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
	return 'My dashboard'

@main_bp.route('/logout', methods=['GET'])
@login_required
def logout():
	logout_user()
	return redirect('/')
