from flask import Blueprint, request, current_app, render_template, redirect

# Create a blueprint called 'common', which contains the main page and other public pages
common = Blueprint('common',__name__,url_prefix='/')

@common.route('')
def index():
	return render_template('index.html', current_user='Xiaoming')