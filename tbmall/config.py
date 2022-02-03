class BaseConfig(object):
    # 这里涉及到数据传递，需要设置 SECRET_KEY
    SECRET_KEY = '4bOoOz6GFmF5vVEPd0SvyOOt7m2b16l6'
    # 设置服务监听地址：http://0.0.0.0:5020
    LISTENER = ('0.0.0.0', 5020)

    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root:Pa$$w0rd@localhost:3306/ebmall?charset=utf8' # Need to encode the db password
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