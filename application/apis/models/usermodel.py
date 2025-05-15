from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# create table administrators(
# idAdministrator serial primary key,
# adminName varchar(30) not null,
# adminLastname varchar(30) not null,
# adminPhone varchar(10) not null,
# adminEmail varchar(50) not null,
# adminPass varchar(100) not null,
# adminStatus bool default true,
# dateCreated timestamp default current_timestamp
# );

class User(Base):
    __tablename__ = "users"

    idadministrator = Column(Integer, primary_key=True, index=True)
    adminname = Column(String)
    adminlastname = Column(String)
    adminemail = Column(String, unique=True, index=True)
    adminpass = Column(String)
    adminphone = Column(String)
    adminstatus = Column(Boolean)
    admincreated = Column(DateTime)