from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, CheckConstraint, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os

load_dotenv()

Base = declarative_base()
GLOBAL_SALT = os.getenv("GLOBAL_SALT")


class review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    comment = Column(Text, nullable=False)
    rating = Column(Integer, CheckConstraint('rating  >= 0 AND rating  <= 10'))

    created_at = Column(DateTime(timezone=True), server_default=func.timezone('UTC', func.now()))
    updated_at = Column(DateTime(timezone=True), server_default=func.timezone('UTC', func.now()),
                        onupdate=func.timezone('UTC', func.now()))

    product_id = Column(Integer, ForeignKey('products.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    product = relationship("product", back_populates="reviews")
    user = relationship("User", back_populates="reviews")
