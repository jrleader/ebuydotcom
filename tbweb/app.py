from flask import Flask, render_template
from . import config

app_name = 'ebuydotcom'

def init_handler(app):
	from .handlers import init
	init(app)

app = Flask(app_name, template_folder='./templates', static_folder='./static')

app.config.from_object(config.configs.get(app.env))

init_handler(app)

@app.errorhandler(404)
def page_not_found(e):
	return render_template('error.html', current_user='None', error=e)

@app.errorhandler(500)
def int_serv_err(e):
	return render_template('error.html', current_user='None', error=e)


if __name__ == '__main__':
	# app.run(debug=True)

	from gevent import pywsgi
	# 如果是以“python -m tbweb.app”的方式运行，则页面的访问地址应该是：http://0.0.0.0:5050
	server = pywsgi.WSGIServer(app.config['LISTENER'], app)
	print('gevent WSGIServer listen on {} ...'.format(app.config['LISTENER']))
	server.serve_forever()

