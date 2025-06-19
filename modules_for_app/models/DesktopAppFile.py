import enum
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, CheckConstraint, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from OS import OSType
import os

load_dotenv()

Base = declarative_base()
GLOBAL_SALT = os.getenv("GLOBAL_SALT")


class DesktopAppFile(Base):
    __tablename__ = 'desktopappfiles'

    id = Column(Integer, primary_key=True)
    version = Column(String(20), nullable=False)
    file_url=Column(String(50),nullable=False)
    os_type = Column(Enum(OSType), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.timezone('UTC', func.now()))
    updated_at = Column(DateTime(timezone=True), server_default=func.timezone('UTC', func.now()),
                        onupdate=func.timezone('UTC', func.now()))


