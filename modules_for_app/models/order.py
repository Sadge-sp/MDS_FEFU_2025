from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime, Enum, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum
import datetime

Base = declarative_base()

# 💡 Перечисления для статуса, доставки и оплаты (удобно и безопасно)
class OrderStatus(enum.Enum):
    PENDING = "pending"
    PAID = "paid"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELED = "canceled"

class DeliveryMethod(enum.Enum):
    PICKUP = "pickup"
    COURIER = "courier"
    POST = "post"

class PaymentMethod(enum.Enum):
    CARD = "card"
    CASH = "cash"
    ONLINE = "online"

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    total_price = Column(Float, nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING, nullable=False)
    delivery_method = Column(Enum(DeliveryMethod), nullable=False)
    payment_method = Column(Enum(PaymentMethod), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.timezone('UTC', func.now()))
    updated_at = Column(DateTime(timezone=True), server_default=func.timezone('UTC', func.now()), onupdate=func.timezone('UTC', func.now()))

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
