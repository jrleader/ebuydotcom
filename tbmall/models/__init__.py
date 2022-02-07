# __init__.py

from .product import Product, ProductSchema
from .shop import Shop, ShopSchema
from .favourite_product import FavouriteProduct, FavouriteProductSchema

from sqlalchemy.orm import sessionmaker, Session

from sqlalchemy import create_engine

from ..config import BaseConfig

engine = create_engine(BaseConfig.SQLALCHEMY_DATABASE_URI, echo=True)
sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

session = Session() # 先创建好Session便于引用

def get_db_session():
    global session
    session = sessionlocal()
    try:
        yield session
    finally:
        session.close()

get_db_session() # 创建和engine绑定的session，该session会在tblib.model类中被读取到