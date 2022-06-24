# app.py

from flask import Flask 

from . import config

ENV = 'development'

def init_mongo(app):
	from tblib.mongo import init

	init(app)

def init_handler(app):
	from .handlers import init

	init(app)

app = Flask(__name__)

# Load config from file
# app.config.from_object(config.configs.get(app.env))
app.config.from_object(config.configs.get(ENV))


init_mongo(app)

init_handler(app)

print('app {} started with config\n LISTENER: {}, MONGO_URI: {}'.format(app.name, app.config.get('LISTENER'), app.config.get('MONGO_URI')))

if __name__ == '__main__': # If running the app by invoking "python -m tbfile.app"
	from gevent import pywsgi

	server = pywsgi.WSGIServer(app.config['LISTENER'], app) # Run the app in a container

	print('gevent WSGIServer listen on {} ...'.format(app.config['LISTENER']))

	server.serve_forever() # Start listening to http requests