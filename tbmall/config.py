from .utils.utils import Cryptog as cg

class BaseConfig(object):
    # 这里涉及到数据传递，需要设置 SECRET_KEY
    # 用于登录身份验证
    SECRET_KEY = '4bOoOz6GFmF5vVEPd0SvyOOt7m2b16l6'
    # 设置服务监听地址：http://0.0.0.0:5020
    LISTENER = ('0.0.0.0', 5020)

    # 在变量被初始化后即被读取，后续对该变量的更改无效
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root:{}@localhost:3306/ebmall?charset=utf8'.format(cg.decrypt_encoded_info('eee942b5ad7245dffe7731380e2b57fc')) # Need to encode the db password

    SQLALCHEMY_TRACK_MODIFICATIONS = False # 在不需要跟踪对象变化时降低内存消耗. Flask-SQLAlchemy官方建议

    PAGINATION_PER_PAGE = 20 # 列表接口默认返回的每页数据条数



class DevelopmentConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    pass


configs = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}