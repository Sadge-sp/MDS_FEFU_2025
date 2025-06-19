from sqlalchemy import Column, Integer, ForeignKey, Float, func, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class OrderItem(Base):
    __tablename__ = 'orderitems'

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    configuration_id = Column(Integer, ForeignKey('mouse_configurations.id'), nullable=True)
    quantity = Column(Integer, default=1, nullable=False)
    price = Column(Float, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.timezone('UTC', func.now()))
    updated_at = Column(DateTime(timezone=True), server_default=func.timezone('UTC', func.now()), onupdate=func.timezone('UTC', func.now()))


    order = relationship("Order", back_populates="items")
    product = relationship("product", back_populates="order_items")
    configuration = relationship("MouseConfiguration", back_populates="order_item")
