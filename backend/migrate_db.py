#!/usr/bin/env python3
"""
Database migration script for MindfulWealth application
"""
import os
import sys
import pathlib
import sqlite3
from sqlalchemy import create_engine, inspect
from dotenv import load_dotenv

# Add the current directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Import models after adding current directory to path
from models import Base, User, Transaction, Budget, SavedImpulse

# Load environment variables
load_dotenv()

def get_db_path():
    """Get the database path from environment or use default"""
    DB_PATH = os.getenv('DB_PATH', 'mindfulwealth.db')
    return pathlib.Path(__file__).parent / DB_PATH

def backup_database():
    """Create a backup of the existing database"""
    db_path = get_db_path()
    backup_path = db_path.with_suffix('.db.backup')
    
    if db_path.exists():
        import shutil
        shutil.copy2(db_path, backup_path)
        print(f"Database backup created at {backup_path}")
    else:
        print("No existing database found, skipping backup")

def check_table_exists(conn, table_name):
    """Check if a table exists in the database"""
    cursor = conn.cursor()
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
    return cursor.fetchone() is not None

def check_column_exists(conn, table_name, column_name):
    """Check if a column exists in a table"""
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()
    return any(column[1] == column_name for column in columns)

def recreate_users_table(conn):
    """Recreate the users table with the updated schema"""
    print("Recreating users table...")
    
    # Create a temporary table with the new schema
    conn.execute('''
    CREATE TABLE users_new (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE,
        password_hash TEXT,
        is_demo BOOLEAN DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        theme_preference TEXT DEFAULT 'dark',
        layout_preference TEXT DEFAULT 'gradient',
        language_preference TEXT DEFAULT 'fr',
        personality_preference TEXT DEFAULT 'nice'
    )
    ''')
    
    # Copy data from the old table to the new one
    try:
        # First check if the old table has all the columns
        columns = conn.execute("PRAGMA table_info(users)").fetchall()
        column_names = [column[1] for column in columns]
        
        # Build the column list for the INSERT statement
        old_columns = []
        new_columns = []
        
        # Always include these core columns
        core_columns = ['id', 'name', 'email', 'password_hash', 'is_demo', 'created_at', 'last_login']
        for col in core_columns:
            if col in column_names:
                old_columns.append(col)
                new_columns.append(col)
        
        # Check for preference columns
        preference_columns = {
            'theme_preference': 'dark',
            'layout_preference': 'gradient',
            'language_preference': 'fr',
            'personality_preference': 'nice'
        }
        
        for col, default in preference_columns.items():
            if col in column_names:
                old_columns.append(col)
                new_columns.append(col)
            else:
                # If the column doesn't exist in the old table, use a default value
                new_columns.append(f"'{default}' AS {col}")
        
        # Build and execute the INSERT statement
        insert_sql = f'''
        INSERT INTO users_new ({', '.join(new_columns)})
        SELECT {', '.join(old_columns if len(old_columns) == len(new_columns) else new_columns)}
        FROM users
        '''
        
        conn.execute(insert_sql)
        print(f"Copied {conn.execute('SELECT COUNT(*) FROM users_new').fetchone()[0]} rows to new users table")
        
    except Exception as e:
        print(f"Error copying data to new users table: {e}")
        raise
    
    # Drop the old table and rename the new one
    conn.execute("DROP TABLE users")
    conn.execute("ALTER TABLE users_new RENAME TO users")
    print("Users table recreated successfully")

def recreate_saved_impulses_table(conn):
    """Recreate the saved_impulses table with the new schema"""
    # Check if the table exists
    if not check_table_exists(conn, 'saved_impulses'):
        print("saved_impulses table doesn't exist, skipping recreation")
        return
        
    # Get existing data
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM saved_impulses;")
    impulses_data = cursor.fetchall()
    
    # Get column names
    cursor.execute("PRAGMA table_info(saved_impulses);")
    columns = cursor.fetchall()
    column_names = [column[1] for column in columns]
    
    # Create a temporary table with the new schema
    cursor.execute("""
    CREATE TABLE saved_impulses_new (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        description TEXT NOT NULL,
        amount FLOAT NOT NULL,
        category TEXT,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        projected_value_1yr FLOAT NOT NULL,
        projected_value_5yr FLOAT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    );
    """)
    
    # Copy data from old table to new table
    for impulse in impulses_data:
        # Create a dictionary of column name to value
        impulse_dict = {column_names[i]: impulse[i] for i in range(len(column_names))}
        
        # Handle column name differences
        if 'item' in impulse_dict and 'description' not in impulse_dict:
            impulse_dict['description'] = impulse_dict['item']
        
        if 'potential_value' in impulse_dict and 'projected_value_1yr' not in impulse_dict:
            impulse_dict['projected_value_1yr'] = impulse_dict['potential_value']
            # Set a default value for projected_value_5yr if it doesn't exist
            if 'projected_value_5yr' not in impulse_dict:
                impulse_dict['projected_value_5yr'] = float(impulse_dict['potential_value']) * (1.07 ** 5)
        
        # Determine which columns to insert
        valid_columns = []
        valid_values = []
        
        for col in ['id', 'user_id', 'description', 'amount', 'category', 'date', 'projected_value_1yr', 'projected_value_5yr']:
            if col in impulse_dict:
                valid_columns.append(col)
                valid_values.append(impulse_dict[col])
            elif col == 'description' and 'item' in impulse_dict:
                valid_columns.append('description')
                valid_values.append(impulse_dict['item'])
            elif col == 'projected_value_1yr' and 'potential_value' in impulse_dict:
                valid_columns.append('projected_value_1yr')
                valid_values.append(impulse_dict['potential_value'])
            elif col == 'projected_value_5yr' and 'potential_value' in impulse_dict:
                valid_columns.append('projected_value_5yr')
                valid_values.append(float(impulse_dict['potential_value']) * (1.07 ** 5))
        
        if valid_columns:
            placeholders = ", ".join(["?" for _ in range(len(valid_columns))])
            columns_str = ", ".join(valid_columns)
            
            cursor.execute(f"INSERT INTO saved_impulses_new ({columns_str}) VALUES ({placeholders});", valid_values)
    
    # Drop the old table
    cursor.execute("DROP TABLE saved_impulses;")
    
    # Rename the new table to the original name
    cursor.execute("ALTER TABLE saved_impulses_new RENAME TO saved_impulses;")
    
    print("saved_impulses table recreated with new schema")

def migrate_database():
    """Migrate the database to the latest schema"""
    db_path = get_db_path()
    
    # Create a SQLite connection
    conn = sqlite3.connect(db_path)
    
    try:
        # Check if users table exists
        if check_table_exists(conn, 'users'):
            # Check if any of the new columns are missing
            missing_columns = []
            for column_name in ['email', 'password_hash', 'is_demo', 'created_at', 'last_login']:
                if not check_column_exists(conn, 'users', column_name):
                    missing_columns.append(column_name)
            
            # If any columns are missing, recreate the table
            if missing_columns:
                print(f"Missing columns in users table: {', '.join(missing_columns)}")
                recreate_users_table(conn)
        
        # Check if saved_impulses table exists and migrate if needed
        if check_table_exists(conn, 'saved_impulses'):
            # Check for column name discrepancies
            has_description = check_column_exists(conn, 'saved_impulses', 'description')
            has_item = check_column_exists(conn, 'saved_impulses', 'item')
            
            has_projected_value_1yr = check_column_exists(conn, 'saved_impulses', 'projected_value_1yr')
            has_potential_value = check_column_exists(conn, 'saved_impulses', 'potential_value')
            
            # If there's a mismatch between model and database column names, recreate the table
            if (has_item and not has_description) or (has_potential_value and not has_projected_value_1yr):
                print("Column name discrepancies found in saved_impulses table")
                recreate_saved_impulses_table(conn)
        
        # Commit changes
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error during migration: {e}")
        raise
    finally:
        conn.close()
    
    # Now use SQLAlchemy to ensure all tables are created
    DATABASE_URL = f"sqlite:///{db_path}"
    engine = create_engine(DATABASE_URL)
    
    # Create any missing tables
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    
    # Get all model tables
    model_tables = [model.__tablename__ for model in [User, Transaction, Budget, SavedImpulse]]
    
    # Create missing tables
    for table_name in model_tables:
        if table_name not in existing_tables:
            print(f"Creating table '{table_name}'")
    
    # Create all tables that don't exist yet
    Base.metadata.create_all(engine)
    
    print("Database migration completed successfully")

if __name__ == "__main__":
    print("Starting database migration...")
    
    # Create a backup of the existing database
    backup_database()
    
    # Migrate the database
    migrate_database()
    
    print("Migration completed successfully!") 