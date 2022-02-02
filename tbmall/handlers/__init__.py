import flask.app
from tblib.handler import handle_error_json

from .product import product
from .shop import shop
# from .favourite_product import favourite_product
from .favourite_product import fav_product


def init(app):

    '''
    注册错误处理类和蓝本
    '''
    app.register_error_handler(Exception, handle_error_json) # 为Exception的所有子类注册错误处理器

    app.register_blueprint(product)
    app.register_blueprint(shop)
    # app.register_blueprint(favourite_product)
    app.register_blueprint(fav_product)
    