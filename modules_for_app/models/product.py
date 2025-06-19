from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, CheckConstraint, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash,  check_password_hash
from dotenv import load_dotenv
import os
load_dotenv()

Base = declarative_base()
GLOBAL_SALT = os.getenv("GLOBAL_SALT")
class product(Base):
    __tablename__ = 'products'  # название таблицы в БД

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    description= Column(Text, nullable=False)
    price= Column(Integer,CheckConstraint('price >= 1 AND price <= 999999') )
    image_url = Column(String(255),nullable=True)
    stock = Column(Integer,CheckConstraint('stock>= 0 AND stock> <= 99999999'))
    rating = Column(Integer,CheckConstraint('rating  >= 0 AND rating  <= 10'))

    created_at = Column(DateTime(timezone=True), server_default=func.timezone('UTC', func.now()))
    updated_at = Column(DateTime(timezone=True), server_default=func.timezone('UTC', func.now()),
                        onupdate=func.timezone('UTC', func.now()))


    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship("category", back_populates="products")
    reviews = relationship("review", back_populates="product")
    order_items = relationship("OrderItem", back_populates="product")