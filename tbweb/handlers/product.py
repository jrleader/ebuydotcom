# handlers/product.py

from flask import Blueprint, render_template, redirect, request, current_app

from ..services import EbFile, EbMall, EbBuy

from ..config import BaseConfig

base_url_mall = BaseConfig.SERVICE_TBMALL['addresses'][0]

product = Blueprint('products', __name__, url_prefix='/products')

@product.route('', methods=['GET'])
def index():
    '''
    商品列表页
    '''
    page = request.args.get('page', 1, type=int) # 当前要显示的页面，默认为第一页

    lim = request.args.get('limit', current_app.config['PAGINATION_PER_PAGE'], type=int)

    offset = (page - 1) * lim

    resp = EbMall(current_app).get_json('{}/products'.format(base_url_mall), params= {
        'limit': lim,
        'offset': offset
    })

    prods = resp['data']

    return render_template('product/index.html', **prods)

@product.route('/<int:id>', methods=['GET'])
def detail(id):
    '''
    商品详情页
    '''

    resp = EbMall(current_app).get_json('{}/products/{}'.format(base_url_mall, id))

    prod = resp['data']

    return render_template('product/detail.html', **prod)