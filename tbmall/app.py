from flask import Flask

from . import config

import sys  
from pathlib import Path  

def init_model(app):
    from tblib.model import init # ImportError: attempted relative import with no known parent package

    from importlib import import_module

    # model.init(app)
    init(app)

    import_module('.models',__package__) # 在初始化数据库后导入商城模型


def init_handler(app):
    from .handlers import init

    init(app)

# 把项目根目录添加到path，避免在引用时找不到对应package
file = Path(__file__).resolve()  
# print(file)
package_root_directory = file.parents[1]  

# print(package_root_directory)
sys.path.append(str(package_root_directory))  

# 创建Flask app
app = Flask(__name__)

app.config.from_object(config.configs.get(app.env))

init_model(app),

init_handler(app)

# 通过python -m app命令运行时调用
if __name__ == '__main__':
    from gevent import pywsgi
    # 如果是以“python -m tbmall”的方式运行，那么服务监听的地址为：http://0.0.0.0:5020
    server = pywsgi.WSGIServer(app.config['LISTENER'], app)
    print('gevent WSGIServer listen on {} ...'.format(app.config['LISTENER']))
    server.serve_forever()
