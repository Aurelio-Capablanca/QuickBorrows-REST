from sqlalchemy import Column, Integer, DateTime, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BorrowFundsHistoric(Base):
    __tablename__ = "borrowfundshistory"

    idfound = Column(Integer, primary_key=True, index=True)
    amountfound = Column(Float)
    pastamount = Column(Float)
    datecreated = Column(DateTime)
    idadministrator = Column(Integer)
    idorigin = Column(Integer)
    isinput = Column(Boolean)
