from flask import Flask, render_template

app_name = 'tbecom'

app = Flask(app_name, template_folder='./tbweb/templates', static_folder='./tbweb/static')

def init_handler(app):
	from tbweb.handlers import init
	init(app)


init_handler(app)

@app.errorhandler(404)
def page_not_found(e):
	return render_template('error.html', current_user='None', error=e)

@app.errorhandler(500)
def int_serv_err(e):
	return render_template('error.html', current_user='None', error=e)


if __name__ == '__main__':
	app.run(debug=True)

