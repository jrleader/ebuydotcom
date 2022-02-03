# model.py

# Initialization of the connection object that connects to SQLAlchemy

from sqlalchemy.orm.session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# The vars are initialized here so that the IDE can infer the types of those objects and thus
# autocompletion can be used 
db = SQLAlchemy() 
session = Session()
migrate = Migrate()

def init(app):
	# Will only be fully initialized after the Flask app is started
	global db,session,migrate 

	db=SQLAlchemy(app)
	print('Connected to database {}'.format(db))
	session = db.session
	migrate = Migrate(app, db)