from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from .database import Base
import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    dossiers = relationship("Dossier", back_populates="owner")

class Dossier(Base):
    __tablename__ = "dossiers"
    id = Column(Integer, primary_key=True, index=True)
    drug_name = Column(String)
    impact_score = Column(Integer)
    metrics = Column(JSON) # Stores the comparison table data [cite: 126]
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="dossiers")