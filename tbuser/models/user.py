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

    _password = Column('password_hash', String(128), nullable=False) # 只存储密码散列值，不存储密码本身

    # 头像图片地址
    avatar = Column(String(200), nullable=False, default='') 

    gender = Column(String(1), nullable=False)

    mobile = Column(String(11), unique=True)

    wallet_money = Column(Integer, nullable=False, default=0)

    @property
    def password(self):
        raise AttributeError("Password is not accessible!")

    @password.setter
    def password(self, password):
        # 使用密码加盐哈希函数对输入的密码加密
        self._password = generate_password_hash(password)

    # 核对密码
    def check_password(self, password): 
        '''
        验证用户输入的密码散列值是否与原始密码散列值一致
        '''
        return check_password_hash(self._password, password)

class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    _password = fields.Str()
    avatar = fields.Str()
    gender = fields.Str()
    mobile = fields.Str()
    wallet_money = fields.Int()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)