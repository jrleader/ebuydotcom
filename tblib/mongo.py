# Initialization of MongoDB access object

from flask_pymongo import PyMongo

mongo = PyMongo()

def init(app):
	global mongo

	mongo = PyMongo(app)