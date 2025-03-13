#!/usr/bin/env python3
"""
Fix database script for MindfulWealth application
This script will update the database schema and reinitialize the database
"""
import os
import sys
import pathlib
import shutil
import sqlite3
from datetime import datetime

# Add the current directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

def get_db_path():
    """Get the database path"""
    DB_PATH = pathlib.Path(__file__).parent / "mindfulwealth.db"
    return DB_PATH

def backup_database():
    """Create a backup of the database"""
    db_path = get_db_path()
    if not db_path.exists():
        print(f"Database file not found at {db_path}")
        return False
    
    # Create a backup with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = db_path.with_name(f"mindfulwealth_backup_{timestamp}.db")
    
    try:
        shutil.copy2(db_path, backup_path)
        print(f"Database backed up to {backup_path}")
        return True
    except Exception as e:
        print(f"Error backing up database: {e}")
        return False

def fix_database():
    """Fix the database by updating the schema directly"""
    print("Starting database fix process...")
    
    # First, backup the database
    if not backup_database():
        response = input("Failed to backup database. Continue anyway? (y/n): ")
        if response.lower() != 'y':
            print("Database fix aborted.")
            return
    
    # Connect to the database
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if the personality_preference column exists
        cursor.execute("PRAGMA table_info(users)")
        columns = cursor.fetchall()
        column_names = [column[1] for column in columns]
        
        # Add personality_preference column if it doesn't exist
        if 'personality_preference' not in column_names:
            print("Adding personality_preference column to users table")
            cursor.execute("ALTER TABLE users ADD COLUMN personality_preference TEXT DEFAULT 'nice'")
            
            # Update existing users to use nice personality
            cursor.execute("UPDATE users SET personality_preference = 'nice' WHERE personality_preference IS NULL OR personality_preference = ''")
            
            # Commit the changes
            conn.commit()
            print("Database schema updated successfully")
        else:
            print("personality_preference column already exists")
        
        # Verify the users table structure
        print("\nVerifying users table structure...")
        cursor.execute("PRAGMA table_info(users)")
        columns = cursor.fetchall()
        for column in columns:
            print(f"  {column[1]} ({column[2]})")
        
        # Check if there are any users
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        print(f"\nFound {user_count} users in the database")
        
        if user_count == 0:
            # Create admin user
            print("Creating admin user...")
            import hashlib
            password_hash = hashlib.sha256("password".encode()).hexdigest()
            
            cursor.execute("""
            INSERT INTO users (name, email, password_hash, is_demo, theme_preference, layout_preference, language_preference, personality_preference)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, ("Admin User", "admin@example.com", password_hash, 0, "dark", "gradient", "fr", "nice"))
            
            # Create demo user
            print("Creating demo user...")
            cursor.execute("""
            INSERT INTO users (name, email, is_demo, theme_preference, layout_preference, language_preference, personality_preference)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, ("Demo User", "demo@example.com", 1, "dark", "gradient", "fr", "nice"))
            
            conn.commit()
            print("Users created successfully")
        
    except Exception as e:
        conn.rollback()
        print(f"Error fixing database: {e}")
        print("Database fix failed. Please check the error messages above.")
        return
    finally:
        conn.close()
    
    print("\nDatabase fix completed successfully!")
    print("You can now restart the application.")

if __name__ == "__main__":
    fix_database() 