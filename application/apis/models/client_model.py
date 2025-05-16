from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Clients(Base):
    __tablename__ = "clients"

    idclient = Column(Integer, primary_key=True, index=True)
    clientName = Column(String)
    clientLastname = Column(String)
    clientPhone = Column(String)
    clientEmail = Column(String, unique=True, index=True)
    clientAddress = Column(String)
    clientStatus = Column(Boolean)
    idTypeClient = Column(Integer)
    idRiskClient = Column(Integer)
    idGuarantorClient = Column(Integer, nullable=True)
    isElegible = Column(Boolean)
    isGuarantor = Column(Boolean)
