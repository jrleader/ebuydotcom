# models/shop.py

from sqlalchemy import Column, Integer, String, Index
from sqlalchemy.orm import relationship
from marshmallow import Schema, fields, post_load

from .base import Base


class Shop(Base):
    __tablename__ = 'shops' # 遵循约定，使用复数命名方式
    # 设置索引
    __table_args__ = (
        # 创建普通组合索引, 这里只用到user_id
        Index('idx_user_id', 'user_id'),
        # Index('idx_user_id_and_name', 'name','user_id')
    )

    name = Column(String(200), nullable=False, unique=True)
    description = Column(String(500), nullable=False, default='')
    # 这里的封面图片只是存储通过文件服务返回的图片id值，不存储图片本身
    cover = Column(String(200), nullable=False, default='')
    user_id = Column(Integer, nullable=False) # 为降低服务间的耦合，没有把user_id和User表中的user_id建立外键关系


class ShopSchema(Schema):
    '''
    定义商铺模型类
    '''

    id = fields.Int()
    name = fields.Str()
    description = fields.Str()
    cover = fields.Str()
    user_id = fields.Int()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    @post_load
    def make_shop(self, data, many=False, partial=False):
        '''
        用于反序列化: dict -> obj或string -> obj
        '''
        return Shop(**data)