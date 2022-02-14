from .common import common
from .user import user
from ..models import User

from ..services import EbUser

from ..config import BaseConfig

import traceback

from flask import current_app, render_template
from flask_login import LoginManager

base_url_user =  BaseConfig.SERVICE_TBUSER['addresses'][0]

def init(app):
    app.register_blueprint(common)
    app.register_blueprint(user)

    init_login_manager(app)

def handle_error(error):
    traceback.print_exc()

    return render_template('error.html', error=str(error))

def init_login_manager(app):

    login_mgr = LoginManager()
    login_mgr.init_app(app)     #将login_mgr注册为当前app的login manager
    login_mgr.login_view = 'user.login'
    login_mgr.login_message = '请先登录'
    
    @login_mgr.user_loader
    def user_loader(id): #加载用户对象
        resp = EbUser(current_app).get_json('{}/users/{}'.format(base_url_user, id),check_code=False)
        user = resp['data'].get('user')
        return None if user is None else User(user)




