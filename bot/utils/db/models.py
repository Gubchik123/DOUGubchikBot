from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    BigInteger,
    String,
    Boolean,
    DateTime,
    ForeignKey,
)

from .db import Base
from data.config import DEFAULT_LOCALE


class User(Base):
    """Model for storing information about Telegram users."""

    __tablename__ = "users"
    # Fields from telegram user
    chat_id = Column(BigInteger, primary_key=True, autoincrement=False)
    username = Column(String(32), nullable=True, unique=True)
    full_name = Column(String(110), nullable=True, unique=False)
    # Settings fields
    locale = Column(String(2), nullable=False, default=DEFAULT_LOCALE)
    created = Column(DateTime(timezone=True), server_default=func.now())
    # One-to-one relationship with Job
    job = relationship("Job", uselist=False, backref="user")


class Job(Base):
    """Model for storing job information."""

    __tablename__ = "jobs"

    id_user_id = Column(
        BigInteger,
        ForeignKey("users.chat_id"),
        primary_key=True,
        autoincrement=True,
    )
