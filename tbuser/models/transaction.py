from sqlalchemy import Column, ForeignKey, Integer, String, null, DateTime
from sqlalchemy.orm import relationship, backref

from marshmallow import Schema, fields, post_load

from .base import Base

from .user import UserSchema

class Transaction(Base):

    table_name = '__transactions__'

    # 金额
    amount = Column(Integer, nullable=False) # 当交易发生后用户钱包余额应该被更新

    # 备注
    note = Column(String(200), nullable=False, default='')

    # 付款人
    payer_id = Column(Integer, ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)

    # 收款人
    payee_id = Column(Integer,  ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)

    # 日期
    date = Column(DateTime, nullable=False)

    # 地址
    order_addr = Column(String(200), nullable=False)

    # payee, payer都与User相关，和Transaction是一对多关系
    payee = relationship('User', uselist=False, foreign_keys=[payee_id], backref=backref('payee_transactions', lazy='dynamic'))

    payer = relationship('User', uselist=False, foreign_keys=[payer_id], backref=backref('payer_transactions', lazy='dynamic'))


    # product_ids = Column('String', nullable=False)

    # product = relationship('Product', uselist=True, backref=backref('product_id', lazy='dynamic'))
    # 产品和交易是多对一关系

class TransactionSchema(Schema):
    
    id = fields.Int()
    amount = fields.Int()
    note = fields.Str()
    payer_id = fields.Int()
    payee_id = fields.Int()

    date = fields.DateTime()

    order_addr = fields.Str()

    payer = fields.Nested(UserSchema)
    payee = fields.Nested(UserSchema)

    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    @post_load
    def make_transaction(self, data, **kwargs):
        return Transaction(**data)