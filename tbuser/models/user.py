from psutil import NIC_DUPLEX_UNKNOWN
from sqlalchemy import Column, Integer, String, null
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow import Schema, fields, post_load

from .base import Base

class Gender:
    UNKNOWN = ''
    MALE = 'm'
    FEMALE = 'f'

class User(Base):

    __tablename__ = 'users'

    username = Column(String(20), nullable=False, unique=True)

    # 私有
    _password = Column('password', String(20), nullable=False)

    # 头像图片地址
    avatar = Column(String(200), nullable=False, default='') 

    gender = Column(String(1), nullable=False)

    mobile = Column(String(11), unique=True)

    wallet_money = Column(Integer, nullable=False, default=0)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        # 使用密码加盐哈希函数对输入的密码加密
        self._password = generate_password_hash(password)

    # 核对密码
    def check_password(self, password):
        return check_password_hash(self._password, password)

class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    avatar = fields.Str()
    Gender = fields.Str()
    mobile = fields.Str()
    wallet_money = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)