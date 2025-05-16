from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Clients(Base):
    __tablename__ = "clients"

    idclient = Column(Integer, primary_key=True, index=True)
    clientname = Column(String)
    clientlastname = Column(String)
    clientphone = Column(String)
    clientemail = Column(String, unique=True, index=True)
    clientaddress = Column(String)
    clientstatus = Column(Boolean)
    idtypeclient = Column(Integer)
    idriskclient = Column(Integer)
    idguarantorclient = Column(Integer, nullable=True)
    iselegible = Column(Boolean)
    isguarantor = Column(Boolean)
