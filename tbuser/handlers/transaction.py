# handlers/wallet_transaction.py

from flask import Blueprint, request, current_app
from sqlalchemy import and_, or_

from tblib.model import session
from tblib.handler import json_response, ResponseCode

from ..models import Transaction, TransactionSchema, User
# from ..models import get_db_session

transaction = Blueprint(
    'wallet_transaction', __name__, url_prefix='/wallet_transactions')

# session = list(get_db_session()).pop(0)

@transaction.route('', methods=['POST'])
def create_wallet_transaction():
    '''
    创建交易
    '''
    
    trans_data = request.get_json()

    # 反序列化
    trans = TransactionSchema.load(trans_data)

    # 采用乐观锁来防止并发情况下可能出现的数据不一致性，也可使用悲观锁（query 时使用 with_for_update），但资源消耗较大 (详情参考https://docs.sqlalchemy.org/en/14/orm/query.html)
    # 查看付款人 payer 是否存在，如果不存在则返回不存在
    payer = User.query.get(trans.payer_id)

    if payer == None:
        return json_response(ResponseCode.NOT_FOUND)

    # 查看收款人payee是否存在
    payee = User.query.get(trans.payee_id)
    if payee == None:
        return json_response(ResponseCode.NOT_FOUND)
    
    # 对收款人和付款人的钱包余额进行更新

    # 更新付款人的钱包余额

    # 采用乐观锁方式，检查更新余额前付款人的钱包余额与当前钱包余额是否相同，如果相同就更新
    updated_count = User.query.filter(and_(User.id == payer,User.wallet_money >= trans.amount, User.wallet_money == payer.wallet_money)).update({User.wallet_money: payer.wallet_money - trans.amount})
    
    # 更新失败，回滚事务
    if(updated_count == 0):
        session.rollback()
        return json_response(ResponseCode.TRANSACTION_FAILURE)

    # 用和上述同样的方式更新收款人的钱包余额
    updated_count = User.query.filter(and_(User.id == payee,User.wallet_money >= trans.amount)).update({User.wallet_money: payee.wallet_money + trans.amount})

    # 更新失败，回滚事务
    if(updated_count == 0):
        session.rollback()
        return json_response(ResponseCode.TRANSACTION_FAILURE)

    # 将交易存入数据库
    session.add(trans)
    session.commit()

    # 返回交易数据
    return json_response(wallet_transaction=TransactionSchema().dump(trans))


@transaction.route('', methods=['GET'])
def get_transactions_list():
    '''
    获取交易列表, 可按user_id过滤
    '''
    user_id = request.args.get('user_id', type=int)
    order_direction = request.args.get('order_direction', 'desc')
    limit = request.args.get(
        'limit', current_app.config['PAGINATION_PER_PAGE'], type=int)
    offset = request.args.get('offset', 0, type=int)

    order_by = Transaction.id.asc(
    ) if order_direction == 'asc' else Transaction.id.desc()
    query = Transaction.query

    total = query.count

    # 如果用户id非空，那么当该id等于payer或payee id时就启动查询
    if user_id != None:
        query = query.filter(or_(query.payer_id == user_id, query.payee_id == user_id))

        total = query.count

    res = query.limit(limit)\
                .order_by(order_by)\
                .offset(offset)

    return json_response(wallet_transaction=TransactionSchema.dump(res, many=True), total = total)
                    
    

@transaction.route('/<int:id>', methods=['POST'])
def update_transaction(id):
    '''
    更新交易
    '''
    trans = Transaction.query.get(id)
    if trans == None:
        return json_response(ResponseCode.NOT_FOUND)

    data = request.get_json()
    
    for k,v in data.items():
        setattr(trans, k, v) # 调用内置函数设置待更新的user属性
    
    # 更新数据库
    session.commit()

    return json_response(wallet_transaction = TransactionSchema().dump(trans), message='Transaction {} has been updated!'.format(id))
    


@transaction.route('/<int:id>', methods=['GET'])
def get_transaction_by_id(id):
    '''
    按id获取交易
    '''
    trans = Transaction.query.get(id)

    if trans == None:
        return json_response(ResponseCode.NOT_FOUND)
    
    return json_response(wallet_transaction = TransactionSchema().dump(trans))
    

@transaction.route('/<int:id>', methods=['DELETE'])
def del_transaction_by_id(id):
    '''
    按id删除交易
    '''
    pass