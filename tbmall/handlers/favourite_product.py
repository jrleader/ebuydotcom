from flask import Blueprint, request, current_app
from sqlalchemy import and_
from tenacity import retry_never

# from tblib.model import session
from tblib.handler import json_response, ResponseCode

from ..models import FavouriteProduct, FavouriteProductSchema

from ..models import get_db_session

fav_product = Blueprint("favourite_product", __name__, url_prefix='/favourites')

session = next(get_db_session())

@fav_product.route('', methods=['POST'])
def create_fav_product():
    '''
    创建收藏商品
    '''
    data = request.get_json()

    schema = FavouriteProductSchema()

    fav_prod = schema.load(data)

    session.add(fav_prod)

    session.commit()

    return json_response(fav_product = schema.dump(fav_prod))

@fav_product.route('', methods=['GET'])
def get_fav_product_list():
    '''
    获取收藏商品列表, 可根据用户和商品ID筛选
    '''

    # 准备查询参数
    user_id = request.args.get('user_id', type=int)

    prod_id = request.args.get('product_id', type=int)

    order_dir = request.args.get('order_direction', 'desc')

    limit = request.args.get('limit', current_app.config['PAGINATION_PER_PAGE'], type=int)

    offset = request.args.get('offset', 0, type=int)

    order_by = FavouriteProduct.id.asc() if order_dir == 'asc' else FavouriteProduct.id.desc()

    query = FavouriteProduct.query

    if user_id is not None:
        query = query.filter(FavouriteProduct.user_id == user_id)
    elif prod_id is not None:
        query = query.filter(FavouriteProduct.product_id == prod_id)
    # else: return json_response(ResponseCode.NOT_FOUND, message='Favourite product not found with the given user_id and product_id!')

    fav_prod_count = query.count()
    res = query.order_by(order_by)\
                .limit(limit)\
                .offset(offset)
    session.commit()
    return json_response(favourite_product=FavouriteProductSchema().dump(query, many=True), total=fav_prod_count)


@fav_product.route('/<int:id>', methods=['GET'])
def get_fav_product_by_id(id):
    '''
    根据id获取收藏商品
    '''
    query = FavouriteProduct.query
    fav_prod = query.get(id)

    if fav_prod == None:
        return json_response(ResponseCode.NOT_FOUND)

    return json_response(favourite_product=FavouriteProductSchema().dump(fav_prod))


@fav_product.route('/<int:id>', methods=['DELETE'])
def delete_fav_product(id):
    '''
    删除指定id的商品
    '''
    query = FavouriteProduct.query
    fav_prod_to_del = query.get(id)

    if fav_prod_to_del == None:
        return json_response(ResponseCode.NOT_FOUND, message='Favourite product to delete not found with id:{}'.format(id))

    fav_prod_to_del_local = session.merge(fav_prod_to_del)
    
    session.delete(fav_prod_to_del_local)
    session.commit()

    return json_response(favourite_product=FavouriteProductSchema().dump(fav_prod_to_del),delete_count=1)

    