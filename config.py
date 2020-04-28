import os

class Config:
	# Set the secret key to some random bytes. Keep this really secret!
	SECRET_KEY = b'_9#y6K"G4Q0c\n\xec]/'
	#FLASK_APP = Flask(__name__)
	FLASK_ENV = 'development'
	FLASK_DEBUG = 1
	
	DATABASE_URL='mysql://admin:MyPassw0rd#1@localhost/sante_sm_db' #Mysql database
	SQLite_URL = 'sqlite:///database/mydb.db' # Sqlite Database
	SQLALCHEMY_DATABASE_URI = DATABASE_URL
	SQLALCHEMY_TRACK_MODIFICATIONS = False
