from sqlalchemy import Column, Integer, String,Text,Table,ForeignKey
from sqlalchemy.orm import relationship,backref
from database import Base

class User(Base):
  __tablename__ = 'USER'
  id = Column(Integer,primary_key = True, autoincrement=True)
  name = Column(String(50), nullable=False)
  contact_number = Column(String(15))
  email = Column(String(50))

  def __init__(self, name, contact_number = None, email = None):
    self.name = name
    self.contact_number = contact_number
    self.email = email

class FEATURE(Base):
  __tablename__ = 'FEATURE'
  id = Column(Integer, primary_key = True, autoincrement = True)
  name = Column(String(40), nullable = False)
  description = Column(String(500), nullable = False)
  created_by = Column(Integer)
  status = Column(String(20))
  feature_type = Column(String(100))

  def __init__(self, name, description, created_by = 0, status = None, feature_type = None):
    self.name = name
    self.description = description
    self.created_by = created_by
    self.status = status
    self.feature_type = feature_type

class Doctor_Feature(Base):                                       #Association object - for implementing ManytoMany relationship
  __tablename__ = 'DOCTOR_FEATURE_ASSOCIATION'
  id= Column(Integer, primary_key = True)
  user_id = Column(Integer,ForeignKey('USER.id', ondelete='CASCADE'), index = True)
  feature_id = Column(Integer,ForeignKey('FEATURE.id', ondelete='CASCADE'),index = True)
  like = Column(Integer)
  comment = Column(String(200))

  def __init__(self, user_id, feature_id, like = 0, comment = None):
      self.user_id = user_id
      self.feature_id=feature_id
      self.like = like
      self.comment = comment
