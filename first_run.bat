python3 -m venv venv
. venv/bin/activate
pip install Flask
pip install flask-sqlalchemy
pip install mysql
export FLASK_APP=application.py
export FLASK_ENV=development
flask run
