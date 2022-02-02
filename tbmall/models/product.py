# models/product.py

from sqlalchemy import Column, Integer, String, ForeignKey, Index
from sqlalchemy.orm import relationship, backref
from marshmallow import Schema, fields, post_load

from .base import Base
from .shop import ShopSchema


class Product(Base):
    __tablename__ = 'products'
    # 设置索引
    __table_args__ = (
        # 创建普通组合索引
        Index('idx_shop_id', 'shop_id'),
    )

    title = Column(String(200), nullable=False)
    description = Column(String(500), nullable=False, default='')
    # 这里的封面图片只存储通过文件服务返回的图片id值，不存储图片本身
    cover = Column(String(200), nullable=False, default='')
    price = Column(Integer, nullable=False)
    skus_in_stock = Column(Integer, nullable=False)
    shop_id = Column(Integer, ForeignKey(
        'shop.id', ondelete='CASCADE'), nullable=False) # 这里的ondelete参数指如果shop表中的shop_id被删除的话，
        # 那么product表中的也删除
    # shop = relationship('Shop', uselist=False,
                        # backref=backref('products', lazy='dynamic'))
    shop = relationship('Shop', uselist=False,
                        backref=backref('products', lazy='dynamic')) # product和shop是多对一关系，如果把relationship放在shop里那么uselist=False应该移除，这里把relationship和ForeignKey放在一起故保留
    


class ProductSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    cover = fields.Str()
    price = fields.Int()
    skus_in_stock = fields.Int()
    shop_id = fields.Int()
    shop = fields.Nested(ShopSchema)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    @post_load
    def make_product(self, data, many=False, partial=False):
        '''
        用于反序列化: dict -> obj或string -> obj
        '''
        return Product(**data)