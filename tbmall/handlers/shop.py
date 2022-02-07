import json
from flask import Blueprint, request, current_app
from sqlalchemy import or_

from tblib.model import session
from tblib.handler import json_response, ResponseCode

from ..models import Shop, ShopSchema, Product, ProductSchema

# from ..models import session

# session = get_db_session()
# session = next(session)

shop = Blueprint('shop', __name__, url_prefix='/shops')

@shop.route('', methods=['POST'])
def create_shop():
    '''
    创建店铺
    '''

    data = request.get_json() # 通过请求上下文中的request获取包含body的请求，以json表示

    shop = ShopSchema().load(data) # 反序列化
    
    session.add(shop) # 将创建店铺的请求添加到数据库会话

    session.commit()

    return json_response(shop=ShopSchema().dump(shop))

@shop.route('', methods=['GET'])
def shop_list():
    '''
    店铺列表，可根据用户 ID 等条件来筛选
    '''

    print('正在获取店铺列表，当前应用的名称为：{}'.format(current_app.name))

    user_id = request.args.get('user_id', type=int)

    limit = request.args.get('limit', current_app.config['PAGINATION_PER_PAGE'], type=int)
    # 从请求中获取要显示店铺的数目，如果获取不到那么就设置默认值为app配置中的相应项目值

    offset = request.args.get('offset',0,type=int)

    order_dir = request.args.get('order_direction', 'desc')

    order_by = Shop.id.asc() if order_dir == 'asc' else Shop.id.desc()

    # 获取商铺列表的查询语句
    query = Shop.query

    total_no_of_shops = query.count()

    if user_id is not None:
        query = query.filter(Shop.user_id == user_id)
        total_no_of_shops = query.count()
        query = query\
            .order_by(order_by)\
            .limit(limit)\
            .offset(offset)
    # else:
        # return json_response(ResponseCode.NOT_FOUND, 'No matching shop found')


    # 可能返回不止一家店铺，所以many=True
    return json_response(shop=ShopSchema().dump(query, many=True), total=total_no_of_shops)

@shop.route('/<int:id>', methods=['POST'])
def update_shop(id):
    '''根据店铺id更新店铺
    '''
    data = request.get_json()

    query = Shop.query

    updated_count = query.filter(Shop.id == id).update(data)

    if updated_count == 0:
        return json_response(
            ResponseCode.NOT_FOUND
        )
    
    shop = query.get(id) # 异步获取结果？
    session.commit()

    return json_response(shop=ShopSchema().dump(shop))

@shop.route('/<int:id>', methods=['GET'])
def shop_info(id):
    '''
    根据店铺id查询店铺
    '''

    shop = Shop.query.get(id)
    session.commit()

    if shop is None:
        return json_response(ResponseCode.NOT_FOUND)

    return json_response(shop=ShopSchema().dump(shop))

@shop.route('/<int:id>', methods=['DELETE'])
def del_shop(id):
    '''
    根据店铺id删除店铺
    '''
    query = Shop.query

    shop = query.get(id)

    if shop == None:
        return json_response(ResponseCode.NOT_FOUND)

    session.delete(shop)

    session.commit()

    return json_response(deleted_shop = ShopSchema().dump(shop))



