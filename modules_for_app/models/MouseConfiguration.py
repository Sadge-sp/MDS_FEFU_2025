from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, JSON, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()


class MouseConfiguration(Base):
    __tablename__ = 'mouseconfigurations'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    components = Column(JSON, nullable=False)
    preview_image_url = Column(String(50),nullable=True)
    is_draft = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.timezone('UTC', func.now()))
    updated_at = Column(DateTime(timezone=True), server_default=func.timezone('UTC', func.now()),
                        onupdate=func.timezone('UTC', func.now()))

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="mouse_configurations")
    order_item = relationship("OrderItem", back_populates="configuration", uselist=False)
