# shop.py

from flask import Blueprint, render_template, redirect, request, current_app
from graphviz import render

from ..services import EbFile, EbMall, EbUser, EbBuy

from ..config import BaseConfig

shop = Blueprint('shop', __name__, url_prefix='/shops')

base_url_mall = BaseConfig.SERVICE_TBMALL['addresses'][0]
base_url_user = BaseConfig.SERVICE_TBUSER['addresses'][0]


@shop.route('')
def index():
    '''
    店铺列表
    '''
    PRODS_PER_SHOP = 3

    # 获取当前页码编号
    page = request.args.get('page', 1, type=int)

    # 每页要显示的商品数量
    lim = current_app.config['PAGINATION_PER_PAGE']

    # 每页要展示的商品数偏移量, 保证每页的商品可以正常显示
    offset = (page - 1) * lim

    resp = EbMall(current_app).get_json('{}/shops'.format(base_url_mall), params= {
        'limit': lim,
        'offset': offset
    })

    shops = resp['data']['shop']

    total = resp['data']['total']

    # 获取当前页店铺列表的店主信息
    shop_owner_ids = [shop['user_id'] for shop in shops]

    if(len(shop_owner_ids) > 0):
        # 批量获取店主信息
        resp = EbUser(current_app).get_json('{}/users/infos'.format(base_url_user), params=
        {
            'ids':','.join([str(id) for id in shop_owner_ids])
        })
        # 将店主信息赋值给店铺
        for shop in shops:
            owner_id = str(shop['user_id'])
            
            shops['user'] = resp['data']['users'].get(owner_id)
        
    # 获取每个店铺的商品，在店铺列表页每个店铺显示三件

    shop_ids = [shop['id'] for shop in shops]

    if(len(shop_ids) > 0):
        # 批量获取商品信息
        resp = EbMall(current_app).get_json('{}/products/infos'.format(base_url_mall), params= 
        {
            'sids': ','.join([str(id) for id in shop_ids])
        })

        products = resp['data']['products']

        # for s in shops:
            # s['prod_count'] = 0 # 用于追踪需要在商品页面上为每个店铺显示的商品数，单店铺最多三个
        
        # 将商品信息赋予店铺
        for p in products:
            shop = shops.get(str(p['shop_id']))

            products = shop['products']

            if(len(products) < PRODS_PER_SHOP): # 如果商品数小于三个，添加商品到列表
                products.append(p)
                shop['products'] = products
    
    return render_template('shop/index.html', shops=shops, total=total)
            
@shop.route('/<int:id>')
def shop_details(id):
    '''
    店铺详情
    '''

    # 获取与商铺id对应的商铺信息

    resp = EbMall(current_app).get_json('{}/shops/{}'.format(base_url_mall, id))
    shop = resp['data']['shop'] 

    # 获取与商铺id对应的商铺主信息

    resp = EbUser(current_app).get_json('{}/users/{}'.format(base_url_user, str(shop['user_id'])))

    shop_owner = resp['data']['user']

    # 获取店铺商品信息

    page = request.args.get('page', 1, type=int)

    lim = current_app.config['PAGINATION_PER_PAGE']

    offset = (page - 1) * lim

    resp = EbMall(current_app).get_json('{}/products'.format(base_url_mall), params= {
        'shop_id': id,
        'limit': lim,
        'offset': offset
    })

    shop_prods = resp['data']['products']

    return render_template('shops/detail.html', shop=shop, products = shop_prods)
    return render_template('shops/detail.html', shop=shop, **resp['data'])
