from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Text,
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
    vacancy = relationship("Vacancy", uselist=False, backref="user")


class Vacancy(Base):
    """Model for storing vacancy information."""

    __tablename__ = "vacancies"

    id_user_id = Column(
        BigInteger,
        ForeignKey("users.chat_id"),
        primary_key=True,
        autoincrement=True,
    )
    active = Column(Boolean, default=True)
    url_prefix = Column(String(10), default="vacancies")
    last_job_urls = Column(Text, nullable=True)
    # DOU GET request params
    category = Column(String(30), nullable=False)
    exp = Column(String(10), nullable=True)
    city = Column(String(30), nullable=True)
    remote = Column(Boolean, default=False)
    relocate = Column(Boolean, default=False)
    search = Column(Text, nullable=True)
    descr = Column(Boolean, default=False)
