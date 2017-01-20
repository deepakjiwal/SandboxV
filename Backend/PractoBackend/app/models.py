from sqlalchemy import Column,Integer,String,Text,Boolean,Table,ForeignKey
from sqlalchemy.orm import relationship,backref
from database import Base

class User(Base):
  __tablename__ = 'USER'
  practo_id = Column(Integer, primary_key = True)
  name = Column(String(50), nullable=False)
  contact_number = Column(String(15))
  email = Column(String(50))

  def __init__(self, practo_id, name, contact_number = None, email = None):
    self.name = name
    self.practo_id = practo_id
    self.contact_number = contact_number
    self.email = email

class Feature(Base):
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


class User_Feature(Base):                                       #Association object - for implementing ManytoMany relationship
  __tablename__ = 'USER_FEATURE_ASSOCIATION'
  user_id = Column(Integer,ForeignKey('USER.practo_id', ondelete='CASCADE'), primary_key=True)
  feature_id = Column(Integer,ForeignKey('FEATURE.id', ondelete='CASCADE'),primary_key=True)
  liked = Column(Boolean)
  comment = Column(String(200))

  def __init__(self, user_id=0, feature_id=0, liked=False, comment=None):
      self.user_id = user_id
      self.feature_id=feature_id
      self.liked = liked
      self.comment = comment
