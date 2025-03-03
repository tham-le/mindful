"""
Database models for MindfulWealth application
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    """User model representing application users"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    
    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}')>"
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'name': self.name
        }

class Transaction(Base):
    """Transaction model for tracking financial transactions"""
    __tablename__ = 'transactions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    amount = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.now)
    description = Column(String)
    is_impulse = Column(Boolean, default=False)
    
    def __repr__(self):
        return f"<Transaction(id={self.id}, amount={self.amount}, category='{self.category}')>"
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'amount': self.amount,
            'category': self.category,
            'date': self.date.isoformat() if self.date else None,
            'description': self.description,
            'is_impulse': self.is_impulse
        }

class Budget(Base):
    """Budget model for tracking planned vs. actual spending"""
    __tablename__ = 'budgets'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    category = Column(String, nullable=False)
    planned_amount = Column(Float, nullable=False)
    actual_amount = Column(Float, nullable=False)
    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    
    def __repr__(self):
        return f"<Budget(id={self.id}, category='{self.category}', planned={self.planned_amount}, actual={self.actual_amount})>"
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'category': self.category,
            'planned_amount': self.planned_amount,
            'actual_amount': self.actual_amount,
            'month': self.month,
            'year': self.year
        }

class SavedImpulse(Base):
    """SavedImpulse model for tracking redirected impulse purchases"""
    __tablename__ = 'saved_impulses'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    description = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String)
    date = Column(DateTime, default=datetime.now)
    projected_value_1yr = Column(Float, nullable=False)
    projected_value_5yr = Column(Float, nullable=False)
    
    def __repr__(self):
        return f"<SavedImpulse(id={self.id}, description='{self.description}', amount={self.amount})>"
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'item': self.description,  # Renamed for frontend compatibility
            'amount': self.amount,
            'category': self.category,
            'date': self.date.isoformat() if self.date else None,
            'potential_value': self.projected_value_1yr  # Renamed for frontend compatibility
        } 