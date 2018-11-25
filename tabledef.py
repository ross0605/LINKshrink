from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///database.db', echo=True)
Base = declarative_base()


###################################################################
class User(Base):
	""""""
	__tablename__ = "users"

	id = Column(Integer, primary_key=True)
	name = Column(String)
	username = Column(String)
	password = Column(String)

	
	def __init__(self, name, username, password):
		""""""

		self.name = name
		self.username = username
		self.password = password

	def __repr__(self):
		return '{} {} - {}'.format(self.name,self.username,self.password)

class URLTab(Base):
	""""""
	__tablename__ = "urls"
	
	id = Column(Integer, primary_key=True)
	urllong = Column(String)
	urlshort = Column(String)


	def __init__(self, urllong, urlshort):
		""""""

		self.urllong = urllong
		self.urlshort = urlshort

	def __repr__(self):
		return ' {} - {}'.format(self.urllong,self.urlshort)


#Create Tables
Base.metadata.create_all(engine)


