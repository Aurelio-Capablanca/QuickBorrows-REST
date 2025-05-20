from sqlalchemy import Column, Integer, Boolean, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Borrows(Base):
    __tablename__ = "borrows"

    idborrow = Column(Integer, primary_key=True, index=True)
    borrowamount = Column(Float)
    percentagetax = Column(Float)
    totalpayment = Column(Float)
    datetaken = Column(DateTime)
    duedate = Column(DateTime)
    idmethod = Column(Integer)
    idclient = Column(Integer)
    idfound = Column(Integer)
    isactive = Column(Boolean)
