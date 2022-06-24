# shop.py

from flask import Blueprint, render_template, redirect, request, current_app
from graphviz import render

from tblib.service import ServiceResponseNotOk

from ..services import EbFile, EbMall, EbUser, EbBuy

from ..config import BaseConfig

shop = Blueprint('shop', __name__, url_prefix='/shops')

base_url_mall = BaseConfig.SERVICE_TBMALL['addresses'][0]
base_url_user = BaseConfig.SERVICE_TBUSER['addresses'][0]


@shop.route('', methods=['GET'])
def index():
    '''
    店铺列表
    '''
    PRODS_PER_SHOP = 3

    # 获取当前页码编号
    page = request.args.get('page', 1, type=int)

    # 每页要显示的商品数量
    lim = request.args.get('limit', current_app.config['PAGINATION_PER_PAGE'], type=int)

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
            
            shop['user'] = resp['data']['users'].get(owner_id)
        
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
        
        shops_dict = {str(shop['id']): shop for shop in shops}

        # for k,v in shops.items():
        #     print('shop_id: {}, shop_info: {}'.format(k,v))

        # 将商品信息赋予店铺
        for p in products:
            # print(type(products))
            # print(p)
            # print(products[p])
            # print('Current prod: {}'.format(p))
            shop = shops_dict.get(str(products[p]['shop_id']))

            if 'products' in shop.keys():
                products_in_shop = shop['products']
                if(len(products) < PRODS_PER_SHOP): # 如果商品数小于三个，添加商品到列表
                    products_in_shop.append(p)
                    shop['products'] = products_in_shop
            else:
                products_in_shop = []
                products_in_shop.append(p)
                shop['products'] = products_in_shop

        # 遍历商铺列表，并逐个获取商铺所销售商品
        # for shop in shops:
        #     resp = EbMall(current_app).get_json('{}/products'.format(base_url_mall), params={

        #     })
        shops = [shops_dict[i] for i in shops_dict]
        # for i,j in enumerate(shops):
            # print('rendered shop id {}, shop {}'.format(i,j))
    return render_template('shop/index.html', shops=shops, total=total)
            
@shop.route('/<int:id>', methods=['GET'])
def shop_details(id):
    '''
    店铺详情
    '''

    # 获取与商铺id对应的商铺信息

    resp = EbMall(current_app).get_json('{}/shops/{}'.format(base_url_mall, id))
    shop = resp['data']['shop'] 

    # 获取与商铺id对应的商铺主信息

    shop_owner = None

    if shop['user_id']:
        try:
            resp = EbUser(current_app).get_json('{}/users/{}'.format(base_url_user, str(shop['user_id'])))
        except ServiceResponseNotOk as e:
            print(e)

        if 'user' in resp['data']:
            shop_owner = resp['data']['user']

            shop['user'] = shop_owner        
        else:
            shop['user'] = None
    else:
        shop['user'] = None

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
    total_product_count = resp['data']['total']
    # return render_template('shops/detail.html', shop=shop, products = shop_prods)
    # return render_template('shop/detail.html', shop=shop, **resp['data'])
    return render_template('shop/detail.html', shop=shop, products=shop_prods, total=total_product_count)

