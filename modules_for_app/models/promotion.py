from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, CheckConstraint, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os

load_dotenv()

Base = declarative_base()
GLOBAL_SALT = os.getenv("GLOBAL_SALT")


class Promotion(Base):
    __tablename__ = 'promotions'

    id = Column(Integer, primary_key=True)
    comment = Column(Text, nullable=False)
    image_url = Column(String(255), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.timezone('UTC', func.now()))
    updated_at = Column(DateTime(timezone=True), server_default=func.timezone('UTC', func.now()),
                        onupdate=func.timezone('UTC', func.now()))

    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)


