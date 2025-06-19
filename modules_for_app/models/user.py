from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash,  check_password_hash
from dotenv import load_dotenv
import os
load_dotenv()

Base = declarative_base()
GLOBAL_SALT = os.getenv("GLOBAL_SALT")
class User(Base):
    __tablename__ = 'users'  # название таблицы в БД

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(20), nullable=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash= Column(String(255), nullable=False)
    is_email_verified = Column(Boolean, default=False)
    is_phone_verified = Column(Boolean, default=False)
    subscriptions = Column(Boolean, default=False)
    reset_token = Column(String(255), nullable=True)
    reset_token_expires_at = Column(DateTime, nullable=True)
    image_url = Column(String(50),nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.timezone('UTC', func.now()))
    updated_at = Column(DateTime(timezone=True), server_default=func.timezone('UTC', func.now()), onupdate=func.timezone('UTC', func.now()))


    def __repr__(self):
        return f"<User id={self.id} username='{self.username}' email='{self.masked_email()}'>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password + GLOBAL_SALT)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password + GLOBAL_SALT)

    def masked_email(self):
        if not self.email or "@" not in self.email:
            return None
        name, domain = self.email.split("@")
        return f"{name[:2]}****@{domain}"

    mouse_configurations = relationship("MouseConfiguration", back_populates="user")
    orders = relationship("Order", back_populates="user")
    reviews = relationship("Review", back_populates="user")


