from sqlalchemy import Column, Integer, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class IssuedBill(Base):

    __tablename__ = "issuedbill"

    idbill = Column(Integer, primary_key=True, index=True)
    duedate = Column(DateTime)
    amounttopay = Column(Float)
    idplan = Column(Integer)

    def __str__(self):
        return f"Bill #{self.idbill}: Due {self.duedate}, Pay ${self.amounttopay}, Plan {self.idplan}"
