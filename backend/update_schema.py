#!/usr/bin/env python3
"""
Simple script to manually update the database schema to add theme, layout, language and personality preference columns
"""
import sqlite3
import os
import pathlib

def get_db_path():
    """Get the database path"""
    DB_PATH = pathlib.Path(__file__).parent / "mindfulwealth.db"
    return DB_PATH

def update_schema():
    """Update the database schema to add theme, layout, language and personality preference columns"""
    db_path = get_db_path()
    
    if not db_path.exists():
        print(f"Database file not found at {db_path}")
        return
    
    print(f"Updating database schema at {db_path}")
    
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if the columns already exist
        cursor.execute("PRAGMA table_info(users)")
        columns = cursor.fetchall()
        column_names = [column[1] for column in columns]
        
        # Add theme_preference column if it doesn't exist
        if 'theme_preference' not in column_names:
            print("Adding theme_preference column to users table")
            cursor.execute("ALTER TABLE users ADD COLUMN theme_preference TEXT DEFAULT 'dark'")
        else:
            print("theme_preference column already exists")
            # Update existing users to use dark theme
            cursor.execute("UPDATE users SET theme_preference = 'dark' WHERE theme_preference IS NULL OR theme_preference = ''")
        
        # Add layout_preference column if it doesn't exist
        if 'layout_preference' not in column_names:
            print("Adding layout_preference column to users table")
            cursor.execute("ALTER TABLE users ADD COLUMN layout_preference TEXT DEFAULT 'gradient'")
        else:
            print("layout_preference column already exists")
            # Update existing users to use gradient layout
            cursor.execute("UPDATE users SET layout_preference = 'gradient' WHERE layout_preference IS NULL OR layout_preference = ''")
        
        # Add language_preference column if it doesn't exist
        if 'language_preference' not in column_names:
            print("Adding language_preference column to users table")
            cursor.execute("ALTER TABLE users ADD COLUMN language_preference TEXT DEFAULT 'fr'")
        else:
            print("language_preference column already exists")
            # Update existing users to use French language
            cursor.execute("UPDATE users SET language_preference = 'fr' WHERE language_preference IS NULL OR language_preference = ''")
        
        # Add personality_preference column if it doesn't exist
        if 'personality_preference' not in column_names:
            print("Adding personality_preference column to users table")
            cursor.execute("ALTER TABLE users ADD COLUMN personality_preference TEXT DEFAULT 'nice'")
        else:
            print("personality_preference column already exists")
            # Update existing users to use nice personality
            cursor.execute("UPDATE users SET personality_preference = 'nice' WHERE personality_preference IS NULL OR personality_preference = ''")
        
        # Commit the changes
        conn.commit()
        print("Database schema updated successfully")
    
    except Exception as e:
        conn.rollback()
        print(f"Error updating database schema: {e}")
    
    finally:
        conn.close()

if __name__ == "__main__":
    update_schema() 