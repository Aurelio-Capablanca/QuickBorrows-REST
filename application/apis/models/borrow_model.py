from tokenize import Double

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Borrows(Base):

    __tablename__ = "borrows"

    idborrow = Column(Integer, primary_key=True, index=True)
    borrowamount = Column(Double)
    percentagetax= Column(Double)
    datetaken= Column(DateTime)
    duedate= Column(DateTime)
    idmethod= Column(Integer)
    idclient= Column(Integer)
    idfound= Column(Integer)