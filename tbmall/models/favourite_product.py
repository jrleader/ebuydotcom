# models/favorite_product.py

from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import relationship, backref
from marshmallow import Schema, fields, post_load

from .base import Base
from .product import ProductSchema


class FavouriteProduct(Base):
    __tablename__ = 'favorite_products'
    # 在表参数中设置索引
    __table_args__ = (
        # 使用 UniqueConstraint('字段', '字段', name='索引名称') 创建唯一组合索引
        UniqueConstraint('user_id', 'product_id'),
        # 使用 Index('索引名称','字段','字段') 创建普通组合索引
        Index('idx_product_id', 'product_id'),
    )

    user_id = Column(Integer, nullable=False)
    product_id = Column(Integer, ForeignKey(
        'product.id', ondelete='CASCADE'), nullable=False)
    product = relationship('Product', uselist=False, backref=backref('favourites', lazy='dynamic')) 
    # 描述一对多关系，并向Product模型中添加一个属性'favourites'，从而定义反向关系（被多少用户收藏）


class FavouriteProductSchema(Schema):
    id = fields.Int()
    user_id = fields.Int()
    product_id = fields.Int()
    product = fields.Nested(ProductSchema)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    @post_load
    def make_favorite_product(self, data):
        return FavouriteProduct(**data)