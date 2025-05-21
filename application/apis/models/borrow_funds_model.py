from sqlalchemy import Column, Integer, DateTime, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BorrowFunds(Base):

    __tablename__ = "borrowfunds"

    idfound = Column(Integer, primary_key=True, index=True)
    amountfound = Column(Float)
    initialamount = Column(Float)
    datecreated = Column(DateTime)
    idadministrator = Column(Integer)
    isinput = Column(Boolean)

