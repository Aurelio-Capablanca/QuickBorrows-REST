from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Administrators(Base):
    __tablename__ = "administrators"

    idadministrator = Column(Integer, primary_key=True, index=True)
    adminname = Column(String)
    adminlastname = Column(String)
    adminemail = Column(String, unique=True, index=True)
    adminpass = Column(String)
    adminphone = Column(String)
    adminstatus = Column(Boolean)
    datecreated = Column(DateTime)