# config.py

class BaseConfig:
    LISTENER = ('0.0.0.0', 5040) # Address of the file service

    MONGO_URI = 'mongodb://localhost:27017/tbfile'

    def __init__(self) -> None:
        super.__init__()

    def __init__(listener, mongo_uri) -> None:
        super.__init__()
        LISTENER = listener
        MONGO_URI = mongo_uri

class DevelopmentConfig(BaseConfig): # Config for the dev env
    pass

class ProductionConfig(BaseConfig):
    pass

configs = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}