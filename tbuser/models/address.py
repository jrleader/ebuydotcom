from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref
from marshmallow import Schema, fields, post_load

from .base import Base
from .user import UserSchema

class Address(Base):
    __tablename__ = 'addresses'

    address = Column(String(200), nullable=False, unique=True)
    zip_code = Column(String(6), nullable=False, default='')
    phone = Column(String(20), nullable=False)
    is_default = Column(Boolean, nullable=False, default=False)

    # 使用relationship后，Address类可以通过user属性访问User类；使用backref后，User类也可以通过addresses属性访问Address类
    # lazy='dynamic'表示禁止自动查询，用于添加过滤器

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    # Address和User是多对一关系
    user= relationship('User', uselist=False, backref=backref('addresses', lazy='dynamic'))


class AddressSchema(Schema):

    id = fields.Int()
    address = fields.Str()
    zip_code = fields.Str()
    phone = fields.Str()
    is_default = fields.Bool()
    user_id = fields.Int()

    user = fields.Nested(UserSchema)


    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    @post_load
    def make_address(self, data, **kwargs):
        return Address(**data)