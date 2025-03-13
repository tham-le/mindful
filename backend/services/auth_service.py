"""
Authentication service for MindfulWealth application
"""
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models import User
import uuid

class AuthService:
    """Service for handling authentication operations"""
    
    def __init__(self, db_session: Session):
        """Initialize with database session"""
        self.db_session = db_session
    
    def register_user(self, name, email, password):
        """
        Register a new user
        
        Args:
            name (str): User's name
            email (str): User's email
            password (str): User's password
            
        Returns:
            tuple: (success, user_or_error_message)
        """
        try:
            # Check if user with this email already exists
            existing_user = self.db_session.query(User).filter(User.email == email).first()
            if existing_user:
                return False, "Email already registered"
            
            # Create new user
            user = User(name=name, email=email)
            user.set_password(password)
            
            self.db_session.add(user)
            self.db_session.commit()
            
            return True, user
        except IntegrityError:
            self.db_session.rollback()
            return False, "Database error during registration"
        except Exception as e:
            self.db_session.rollback()
            return False, f"Error during registration: {str(e)}"
    
    def login_user(self, email, password):
        """
        Authenticate a user
        
        Args:
            email (str): User's email
            password (str): User's password
            
        Returns:
            tuple: (success, user_or_error_message)
        """
        try:
            user = self.db_session.query(User).filter(User.email == email).first()
            
            if not user:
                return False, "User not found"
                
            if not user.check_password(password):
                return False, "Invalid password"
            
            # Update last login time
            user.last_login = datetime.now()
            self.db_session.commit()
            
            return True, user
        except Exception as e:
            return False, f"Error during login: {str(e)}"
    
    def create_demo_user(self):
        """
        Create a demo user
        
        Returns:
            User: The created demo user
        """
        try:
            demo_user = User.create_demo_user()
            self.db_session.add(demo_user)
            self.db_session.commit()
            return demo_user
        except Exception as e:
            self.db_session.rollback()
            raise e
    
    def get_user_by_id(self, user_id):
        """
        Get user by ID
        
        Args:
            user_id (int): User ID
            
        Returns:
            User: User object if found, None otherwise
        """
        return self.db_session.query(User).filter(User.id == user_id).first() 