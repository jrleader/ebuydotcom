from .common import common

def init(app):
    app.register_blueprint(common)
