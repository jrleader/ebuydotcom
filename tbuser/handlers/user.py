from flask import Blueprint, request, current_app
from sqlalchemy import or_
from werkzeug.exceptions import BadRequest

from tblib.model import session
from tblib.handler import json_response, ResponseCode

from ..models import User, UserSchema, WalletTransaction, WalletTransactionSchema

user = Blueprint('user', __name__, url_prefix='/users')

@user.route('', methods=['POST'])
def create_user():

    data = request.get_json()

    # 为用户添加密码
    password = data.pop('password')
    
    user = UserSchema.load(data)

    user.password = password # 为User设置密码，此时User的set_password方法会被调用，将密码转换为散列值

    session.add(user)

    session.commit()

    return json_response(message='User {} has been created!'.format(data.username), user=UserSchema().dump(data))

@user.route('', methods=['GET'])
def get_users_list():

    '''
    查询用户列表，可根据用户名、手机号等筛选
    '''

    username = request.args.get('username')
    mobile = request.args.get('mobile')

    order_dir = request.args.get('order_direction', 'desc') # 从请求中获取order_direction，默认为desc，即按降序排列

    limit = request.args.get('limit', current_app.config['PAGINATION_PER_PAGE'], type=int) # 从请求中获取结果数量，如果没有就使用配置文件里的默认值

    offset = request.args.get('offset', 0, type=int)

    order_by = User.id.asc() if order_dir == 'asc' else 'desc'

    query = User.query

    # 如果用户名为非空，则按用户名过滤结果
    if username != None:
        query = query.filter(User.username == username)

    # 如果手机号为非空，则按手机号过滤
    if mobile != None:
        query = query.filter(User.mobile == mobile)

    count = query.count()

    # 获取结果
    res = query.order_by(order_by).limit(limit).offset(offset)

    return json_response(users=UserSchema.dump(res, many=True), total = count)

@user.route('/<int:id>', methods=['POST'])
def update_user(id):
    pass

@user.route('/<int:id>', methods=['GET'])
def get_user_by_id(id):
    pass

@user.route('/<int_id>', methods=['DELETE'])
def delete_user(id):
    pass

# @user.route('/<int:id>/verify', methods=['GET']) 
@user.route('/verify', methods=['GET']) # 在发送请求时并不知道用户id，所以从request获取
def verify_user_password(id):
    pass