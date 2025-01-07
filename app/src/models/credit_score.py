from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class CreditScore(Base):
    __tablename__ = "credit_score"

    ref_date = Column(DateTime(255), nullable=True)
    target = Column(Integer(255), nullable=True)
    sexo = Column(Text, nullable=True)
    idade = Column(Float, nullable=True)
    obito = Column(Text, nullable=True)
    uf = Column(Text, nullable=True)
    classe = Column(Text, nullable=True)
