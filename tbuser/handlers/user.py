from flask import Blueprint, request, current_app
from sqlalchemy import or_
from werkzeug.exceptions import BadRequest

from tblib.model import session
from tblib.handler import json_response, ResponseCode

from ..models import User, UserSchema, Transaction, TransactionSchema
# from ..models import get_db_session

user = Blueprint('user', __name__, url_prefix='/users')

# session = next(get_db_session())

@user.route('', methods=['POST'])
def create_user():

    data = request.get_json()

    # 为用户添加密码
    password = data.pop('password')
    
    user = UserSchema().load(data)

    user.password = password # 为User设置密码，此时User的set_password方法会被调用，将密码转换为散列值

    session.add(user)

    session.commit()

    return json_response(message='User {} has been created!'.format(data.get('username')), user=UserSchema().dump(data))

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

    order_by = User.id.asc() if order_dir == 'asc' else User.id.desc()

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

    return json_response(users=UserSchema().dump(res, many=True), total = count)

@user.route('/<int:id>', methods=['POST'])
def update_user(id):

    # 获取待更新的用户信息
    user = User.query.get(id)

    if user == None:
        return json_response(ResponseCode.NOT_FOUND)
    
     # 获取更新数据
    data = request.get_json()

    for k,v in data.items():
        setattr(user, k, v) # 调用内置函数设置待更新的user属性
    
    # 更新数据库
    session.commit()

    return json_response(user = UserSchema().dump(user), message='User {} has been updated!'.format(id))


@user.route('/<int:id>', methods=['GET'])
def get_user_info(id):

    user = User.query.get(id)

    if user == None:
        return json_response(ResponseCode.NOT_FOUND)

    return json_response(user=UserSchema().dump(user))

@user.route('/infos', methods=['GET'])
def get_user_infos():
    '''
    批量查询用户信息
    '''

    ids = []

    for v in request.args.get('ids').split(','):
        id = int(v.strip())
        if id > 0:
            ids.append(id)

    if len(ids) == 0:
        return json_response(ResponseCode.NOT_FOUND)
        
    results = User.query.filter(User.id.in_(ids))

    users = {user.id: UserSchema().dump(user) for user in results}

    return json_response(users=users)

@user.route('/<int_id>', methods=['DELETE'])
def delete_user(id):
    '''
    按用户id移除用户
    '''
    
    user_to_remove = User.query.get(id)

    if user_to_remove == None:
        return json_response(ResponseCode.NOT_FOUND, message='User to remove not found with id {}'.format(id))

    # 规避“Object ... is already attached to session ...问题"
    user_to_remove_local = session.merge(user_to_remove)

    session.delete(user_to_remove_local)
    session.commit()

    return json_response(user = UserSchema().dump(user_to_remove), delete_count=1)

# @user.route('/<int:id>/verify', methods=['GET']) 
@user.route('/verify', methods=['GET']) # 在发送请求时并不知道用户id，所以从request获取
def verify_user_password():
    '''
    核对用户密码
    '''
    username = request.args.get('username')
    password = request.args.get('password')

    if username == None or password == None:
        return json_response(isCorrect=False)
    
    # 返回列表中的首个元素
    user = User.query.filter(User.username == username).first()

    if user == None:
        return json_response(isCorrect=False)

    # 验证密码
    is_correct = user.check_password(password)

    return json_response(isCorrect=is_correct, user=UserSchema().dump(user) if is_correct else None)