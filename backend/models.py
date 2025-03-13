"""
Database models for MindfulWealth application
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    """User model representing application users"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=True)
    password_hash = Column(String, nullable=True)
    is_demo = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    last_login = Column(DateTime, default=datetime.now)
    theme_preference = Column(String, default='dark')
    layout_preference = Column(String, default='gradient')
    language_preference = Column(String, default='fr')
    personality_preference = Column(String, default='nice')
    
    # Relationships
    transactions = relationship("Transaction", back_populates="user")
    saved_impulses = relationship("SavedImpulse", back_populates="user", cascade="all, delete-orphan")
    budgets = relationship("Budget", back_populates="user", cascade="all, delete-orphan")
    
    def set_password(self, password):
        """Set password hash from plain text password"""
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        """Check if provided password matches stored hash"""
        if self.password_hash:
            return check_password_hash(self.password_hash, password)
        return False
    
    @classmethod
    def create_demo_user(cls):
        """Create a demo user with a random name"""
        demo_id = uuid.uuid4().hex[:8]
        return cls(
            name=f"Demo User {demo_id}",
            is_demo=True,
            theme_preference='dark',
            layout_preference='gradient',
            language_preference='fr',
            personality_preference='nice'
        )
    
    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', is_demo={self.is_demo})>"
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'is_demo': self.is_demo,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'theme_preference': self.theme_preference,
            'layout_preference': self.layout_preference,
            'language_preference': self.language_preference,
            'personality_preference': self.personality_preference
        }

class Transaction(Base):
    """Transaction model for tracking user spending"""
    __tablename__ = 'transactions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String(100), nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    description = Column(String(255))
    is_impulse = Column(Boolean, default=False)
    
    # Relationships
    user = relationship("User", back_populates="transactions")
    
    def __init__(self, user_id, amount, category, date=None, description=None, is_impulse=False):
        self.user_id = user_id
        self.amount = amount
        self.category = category
        self.date = date or datetime.utcnow()
        self.description = description
        self.is_impulse = is_impulse
    
    def __repr__(self):
        return f"<Transaction(id={self.id}, category='{self.category}', amount={self.amount})>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'category': self.category,
            'date': self.date.isoformat() if self.date else None,
            'description': self.description,
            'is_impulse': self.is_impulse
        }

class Budget(Base):
    """Budget model for tracking planned spending by category"""
    __tablename__ = 'budgets'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    category = Column(String(100), nullable=False)
    planned_amount = Column(Float, nullable=False)
    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="budgets")
    
    def __init__(self, user_id, category, planned_amount, month, year):
        self.user_id = user_id
        self.category = category
        self.planned_amount = planned_amount
        self.month = month
        self.year = year
    
    def __repr__(self):
        return f"<Budget(id={self.id}, category='{self.category}', planned_amount={self.planned_amount})>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'category': self.category,
            'planned_amount': self.planned_amount,
            'month': self.month,
            'year': self.year
        }

class SavedImpulse(Base):
    """Model for tracking redirected impulse purchases and their projected investment growth"""
    __tablename__ = 'saved_impulses'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    description = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    projected_value_1yr = Column(Float, nullable=False)
    projected_value_5yr = Column(Float, nullable=False)
    notes = Column(Text)
    
    # Relationships
    user = relationship("User", back_populates="saved_impulses")
    
    def __init__(self, user_id, description, category, amount, notes=None):
        self.user_id = user_id
        self.description = description
        self.category = category
        self.amount = amount
        self.notes = notes
        
        # Calculate projected growth (8% annual return)
        self.projected_value_1yr = round(amount * 1.08, 2)
        self.projected_value_5yr = round(amount * (1.08 ** 5), 2)
    
    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'category': self.category,
            'amount': self.amount,
            'date': self.date.isoformat() if self.date else None,
            'projected_value_1yr': self.projected_value_1yr,
            'projected_value_5yr': self.projected_value_5yr,
            'notes': self.notes
        } 