python3 -m venv venv
. venv/bin/activate
pip install Flask
pip install flask-sqlalchemy
pip install flask-login
pip install wtforms
pip install email_validator
pip install mysql
export FLASK_APP=application.py
export FLASK_ENV=development
flask run
