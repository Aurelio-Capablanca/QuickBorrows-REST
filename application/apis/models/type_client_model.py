from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TypeClient(Base):
    __tablename__ = "typeclients"

    idtypeclient = Column(Integer, primary_key=True, index=True)
    typeclient = Column(String)
