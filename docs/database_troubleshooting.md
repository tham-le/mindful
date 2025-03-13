# Database Troubleshooting Guide

This guide provides step-by-step instructions for troubleshooting and resolving common database issues in the MindfulWealth application.

## Common Database Errors

### 1. "no such column" Error

**Error Message:**
```
sqlite3.OperationalError: no such column: users.email
```

**Cause:** The database schema is outdated and missing columns that the application expects.

**Solution:**
1. Run the fix database script:
   ```bash
   chmod +x fix_database.sh
   ./fix_database.sh
   ```
2. Restart the application:
   ```bash
   ./start.sh
   ```

### 2. "Cannot add a UNIQUE column" Error

**Error Message:**
```
sqlite3.OperationalError: Cannot add a UNIQUE column
```

**Cause:** SQLite does not support adding a column with a UNIQUE constraint to an existing table with data.

**Solution:**
1. Run the fix database script:
   ```bash
   chmod +x fix_database.sh
   ./fix_database.sh
   ```
2. Restart the application:
   ```bash
   ./start.sh
   ```

### 3. "no such table" Error

**Error Message:**
```
sqlite3.OperationalError: no such table: users
```

**Cause:** The database is missing tables that the application expects.

**Solution:**
1. Run the fix database script:
   ```bash
   chmod +x fix_database.sh
   ./fix_database.sh
   ```
2. Restart the application:
   ```bash
   ./start.sh
   ```

### 4. Field Name Discrepancies

**Error Message:**
```
KeyError: 'description'
```
or
```
KeyError: 'item'
```

**Cause:** There are field name discrepancies between the frontend and backend models.

**Solution:**
1. Run the fix database script:
   ```bash
   chmod +x fix_database.sh
   ./fix_database.sh
   ```
2. Restart the application:
   ```bash
   ./start.sh
   ```

The application has been updated to handle these field name discrepancies automatically. The backend now accepts both naming conventions:
- `description` or `item` for the saved impulse description
- `projected_value_1yr` or `potential_value` for the projected value after 1 year

## Manual Database Reset

If you want to completely reset the database and start fresh:

1. Stop the application if it's running (Ctrl+C in the terminal where it's running)

2. Delete the existing database file:
   ```bash
   rm backend/mindfulwealth.db
   ```

3. Initialize a new database:
   ```bash
   cd backend
   python init_db.py
   cd ..
   ```

4. Start the application:
   ```bash
   ./start.sh
   ```

## Checking Database Schema

To check the current database schema:

```bash
cd backend
sqlite3 mindfulwealth.db ".schema"
cd ..
```

This will display the SQL statements used to create all tables in the database.

## Backing Up the Database

To manually back up the database:

```bash
cp backend/mindfulwealth.db backend/mindfulwealth.db.backup
```

## Restoring from Backup

To restore the database from a backup:

1. Stop the application if it's running

2. Restore from backup:
   ```bash
   cp backend/mindfulwealth.db.backup backend/mindfulwealth.db
   ```

3. Run migrations to ensure the schema is up to date:
   ```bash
   cd backend
   python migrate_db.py
   cd ..
   ```

4. Start the application:
   ```bash
   ./start.sh
   ```

## Advanced: Manual Migration

If you need to manually migrate the database:

1. Stop the application if it's running

2. Run the migration script:
   ```bash
   cd backend
   python migrate_db.py
   cd ..
   ```

3. Start the application:
   ```bash
   ./start.sh
   ```

## Getting Help

If you continue to experience database issues after trying these solutions, please:

1. Check the application logs for more detailed error messages
2. Refer to the [Database Schema Documentation](database_schema.md) for information about the expected schema
3. Review the [Database Migration Summary](database_migration_summary.md) for insights into how migrations are handled 