import json
from flask import Blueprint, request, current_app
from sqlalchemy import and_, or_

from tblib.model import session
from tblib.handler import json_response, ResponseCode

from ..models import Address, AddressSchema, User

address = Blueprint('address', __name__, url_prefix='/addresses')

@address.route('', methods=['POST'])
def create_addr():
    data = request.get_json()

    addr = AddressSchema().load(data)

    user_id = data.get('user_id')

    # 如果待创建地址是默认地址，那么就把待更新地址的用户的现有的默认地址设为False
    if data.get('is_default'):
        Address.query.filter(and_(Address.is_default == True, Address.user_id == user_id)).update({'is_default':False})

    session.add(addr)
    
    session.commit()

    return json_response(address=AddressSchema().dump(addr))


@address.route('', methods=['GET'])
def get_addr_list():
    '''
    获取地址列表，可按user_id筛选
    '''

    user_id = request.args.get('user_id', type=int)

    limit = request.args.get('limit', current_app.config['PAGINATION_PER_PAGE'], type=int)

    offset = request.args.get('offset', type=int)

    order_dir = request.args.get('order_direction', 'desc', type=str)

    order_by = Address.id.asc() if order_dir == 'asc' else Address.id.desc()

    query = Address.query

    total = query.count

    if user_id != None:
        query = query.filter(Address.user_id == user_id)

        total = query.count
    
    # res = query.limit(limit)
    
    # res = query.from_self().order_by(order_by).offset(offset)

    res = query.order_by(order_by).limit(limit).offset(offset)

    print(res)

    print(total)

    # TypeError: Object of type method is not JSON serializable
    return json_response(address=AddressSchema().dump(res, many=True), total=total) 



@address.route('/<int:id>', methods=['POST'])
def update_addr(id):
    '''
    更新地址
    '''
    addr_to_update = Address.query.get(id)

    if addr_to_update == None:
        return json_response(ResponseCode.NOT_FOUND)
    
    data = request.get_json()

    user_id = addr_to_update.user_id

    # # 如果待更新的地址是默认地址，那么就把待更新地址的用户的现有的默认地址设为False
    # if data.get('is_default'):
    #     Address.query.filter(and_(Address.is_default == True, Address.user_id == user_id)).update({'is_default':False})

    for k,v in data.items():
        setattr(addr_to_update, k, v)
    
    session.commit()

    return json_response(address=AddressSchema().dump(addr_to_update))

@address.route('/<int:id>', methods=['GET'])
def get_addr_by_id(id):
    
    # addr = Address.query.get(id)
    addr = session.query(Address).get(id)

    if addr == None:
        return json_response(ResponseCode.NOT_FOUND)

    return json_response(address=AddressSchema().dump(addr))

@address.route('/infos', methods=['GET'])
def get_addr_infos():
    '''
    批量查询地址
    '''

    ids = []

    for v in request.args.get('ids').split(','):
        id = int(v.strip())

        # query = Address.query.get(id)
        if id > 0:
            ids.append(id)
        
    if len(ids) == 0:
        return json_response(ResponseCode.NOT_FOUND)

    results = Address.query.filter(Address.id.in_(ids))

    # TypeError: Object of type method is not JSON serializable
    
    addrs = {addr.id: AddressSchema().dump(addr) for addr in results}

    return json_response(address=addrs)

@address.route('/<int:id>', methods=['DELETE'])
def del_addr_by_id(id):
    pass
