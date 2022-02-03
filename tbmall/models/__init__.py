# __init__.py

from .product import Product, ProductSchema
from .shop import Shop, ShopSchema
from .favourite_product import FavouriteProduct, FavouriteProductSchema

from sqlalchemy.orm import sessionmaker, Session

from sqlalchemy import create_engine

from ..config import BaseConfig

engine = create_engine(BaseConfig.SQLALCHEMY_DATABASE_URI)
sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()

def get_db_session():
    global session
    session = sessionlocal()
    try:
        yield session
    finally:
        session.close()