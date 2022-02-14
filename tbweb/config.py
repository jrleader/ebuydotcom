# config.py
from .utils import Cryptog as cg

class BaseConfig(object):
    # 用户访问的前端页面的地址为：http://0.0.0.0:5050
    LISTENER = ('0.0.0.0', 5050)
    SECRET_KEY = '4bOoOz6GFmF5vVEPd0SvyOOt7m2b16l6'

    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root:{}@localhost:3306/ebweb?charset=utf8'.format(cg.decrypt_encoded_info('eee942b5ad7245dffe7731380e2b57fc'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SITE_NAME = '易买网'
    PAGINATION_PER_PAGE = 20

    DOMAIN_TBFILE = 'http://localhost:5040'

    SERVICE_TBBUY = {
        'addresses': ['http://localhost:5030'],
    }
    SERVICE_TBFILE = {
        'addresses': ['http://localhost:5040'],
    }
    SERVICE_TBMALL = {
        'addresses': ['http://localhost:5020'],
    }
    SERVICE_TBUSER = {
        'addresses': ['http://localhost:5010'],
    }


class DevelopmentConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    pass


configs = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}