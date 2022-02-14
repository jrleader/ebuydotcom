from werkzeug.exceptions import BadRequest

from flask import Blueprint, request, current_app
from sqlalchemy import or_

from tblib.model import session
# from ..models import get_db_session
from tblib.handler import json_response, ResponseCode

from ..models import Shop, ShopSchema, Product, ProductSchema
# from ..models import session

# 注册蓝本
product = Blueprint('product', __name__, url_prefix='/products')


@product.route('', methods=['POST'])
def create_product():
    '''
    新建商品
    '''

    data = request.get_json()

    pdt_sch = ProductSchema()
    pdt = pdt_sch.load(data)

    session.add(pdt)

    session.commit()

    return json_response(product=pdt_sch.dump(pdt))

@product.route('', methods=['GET'])
def get_product_list():
    '''
    获取商品列表
    '''

    # 配置查询条件
    shop_id = request.args.get('shop_id', type=int)
    limit = request.args.get('limit', current_app.config['PAGINATION_PER_PAGE'], type=int)

    offset = request.args.get('offset', 0, type=int)

    order_dir = request.args.get('order_direction', 'desc')

    order_by = Product.id.asc() if order_dir == 'asc' else Product.id.desc()

    query = Product.query

    total_no_of_prods = query.count()

    if shop_id is not None:
        query = query.filter(Product.shop_id == shop_id)
        total_no_of_prods = query.count()
        query =  query.order_by(order_by)\
                        .limit(limit)\
                        .offset(offset)
    # else:
        # return json_response(ResponseCode.NOT_FOUND, message='No matching products given the shop_id:{}'.format(shop_id))
    
    return json_response(products = ProductSchema().dump(query, many=True), total=total_no_of_prods)

@product.route('/<int:id>', methods=['POST'])
def update_product(id):
    '''
    更新商品
    '''

    # 获取更新数据
    data = request.get_json()

    schema = ProductSchema()

    query = Product.query

    # 根据id更新对应商品
    updated_count = query.filter(Product.id == id).update(data)

    if updated_count == 0: # 不存在商品id为id的商品
        return json_response(ResponseCode.NOT_FOUND)

    session.commit() # 提交查询（！！！）

    # 获取更新后的商品
    new_prod = query.get(id)

    # new_prod = ProductSchema().load(prod)

    return json_response(product=schema.dump(new_prod))

@product.route('/<int:id>', methods=['GET'])
def get_prod_info_by_id(id):
    '''
    按产品id获取产品信息
    '''
    prod = Product.query.get(id)

    if prod == None:
        return json_response(ResponseCode.NOT_FOUND, message='Product not found with id:{}'.format(id))

    return json_response(product=ProductSchema().dump(prod))

@product.route('/infos', methods=['GET'])
def product_infos():
    """批量查询商品，查询指定ID和商品ID列表里的多个商品
    """

    ids = []

    shop_ids = []

    requested_ids =  request.args.get('ids', '').split(',')

    if len(requested_ids) > 0:
        for v in requested_ids:
            id = int(v.strip())
            if id > 0:
                ids.append(id)

    requested_shop_ids = request.args.get('sids','').split(',')

    if len(requested_shop_ids) > 0: # Shop_id是可选参数，如果请求里没有那么不抛出异常
        for v in requested_shop_ids:
            sid = int(v.strip())
            if sid > 0:
                shop_ids.append(sid)
    
    if len(requested_ids) == 0 and len(requested_shop_ids) == 0:
        raise BadRequest()
    
    if len(ids) > 0:
        results = Product.query.filter(Product.id.in_(ids)) # 查找产品id等于id列表中任一的商品

    if len(shop_ids) > 0:
        results = Product.query.filter(Product.shop_id.in_(shop_ids)) # 查找产品所属商铺id属于商铺列表中任一的产品

    products = {product.id: ProductSchema().dump(product) for product in results}

    return json_response(products=products)

@product.route('/<int:id>', methods=['DELETE'])
def remove_product(id):
    '''
    按产品id移除商品
    '''
    # count = Product.query.remove(id)
    prod_to_remove = Product.query.get(id)

    if prod_to_remove == None:
        return json_response(ResponseCode.NOT_FOUND, message='Product to remove not found with id:{}'.format(id))

    # 规避“Object ... is already attached to session ...问题"
    prod_to_remove_local = session.merge(prod_to_remove)
    # session.delete(prod_to_remove)
    session.delete(prod_to_remove_local)
    session.commit()
        
    return json_response(product = ProductSchema().dump(prod_to_remove), delete_count=1)