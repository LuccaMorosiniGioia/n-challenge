from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ConversationHistory(Base):
    __tablename__ = "conv_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(Text, nullable=False)
    role = Column(Text, nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False)
