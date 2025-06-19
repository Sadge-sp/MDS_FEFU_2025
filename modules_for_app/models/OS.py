import enum
from sqlalchemy import Column, Integer, String, Enum, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()


class OSType(enum.Enum):
    WINDOWS = "Windows"
    MAC = "Mac"
    LINUX = "Linux"