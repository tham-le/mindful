"""
Initialize the database with the updated schema
"""
import os
import sys
import pathlib
from sqlalchemy import create_engine, inspect
from dotenv import load_dotenv

# Add the current directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Import models after adding current directory to path
from models import Base, User

# Load environment variables
load_dotenv()

def get_db_path():
    """Get the database path from environment or use default"""
    DB_PATH = os.getenv('DB_PATH', 'mindfulwealth.db')
    return pathlib.Path(__file__).parent / DB_PATH

def init_db():
    """Initialize the database with the updated schema"""
    # Database setup
    DB_PATH = get_db_path()
    DATABASE_URL = f"sqlite:///{DB_PATH}"
    
    # Check if database already exists
    db_exists = DB_PATH.exists()
    
    # Create engine
    engine = create_engine(DATABASE_URL)
    
    if db_exists:
        print(f"Database already exists at {DB_PATH}")
        print("Running migration to ensure schema is up to date...")
        
        # Import and run migration
        try:
            from migrate_db import migrate_database
            migrate_database()
        except ImportError:
            print("Migration script not found. Creating tables if they don't exist.")
            Base.metadata.create_all(engine)
    else:
        # Create tables
        print(f"Creating new database at {DB_PATH}")
        Base.metadata.create_all(engine)
    
    print(f"Database initialized at {DB_PATH}")
    
    return engine

if __name__ == "__main__":
    # Initialize database
    engine = init_db()
    
    # Create a demo admin user for testing
    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Check if admin user already exists
    admin = session.query(User).filter(User.email == "admin@example.com").first()
    
    if not admin:
        admin = User(
            name="Admin User",
            email="admin@example.com",
            is_demo=False
        )
        admin.set_password("password")
        
        session.add(admin)
        session.commit()
        
        print("Admin user created:")
        print(f"  Email: admin@example.com")
        print(f"  Password: password")
    else:
        print("Admin user already exists")
    
    # Create a demo user
    demo = User.create_demo_user()
    session.add(demo)
    session.commit()
    
    print(f"Demo user created: {demo.name}")
    
    session.close() 