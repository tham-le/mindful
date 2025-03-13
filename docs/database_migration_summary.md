# Database Migration Issue Resolution

## Issue Summary

The application encountered a database schema issue when trying to add a new `email` column with a UNIQUE constraint to the existing `users` table. This resulted in the following error:

```
sqlite3.OperationalError: Cannot add a UNIQUE column
```

This error occurs because SQLite does not support adding a column with a UNIQUE constraint to an existing table that already contains data, as it cannot guarantee the uniqueness of the values in the new column.

## Solution Approach

To resolve this issue, we implemented a more robust migration strategy:

1. **Table Recreation**: Instead of trying to add columns with constraints to an existing table, we:
   - Created a new temporary table with the updated schema
   - Copied all existing data from the old table to the new one
   - Dropped the old table
   - Renamed the new table to the original name

2. **Backup System**: Before performing any migration, we implemented an automatic backup system that creates a copy of the current database file.

3. **Error Handling**: We added comprehensive error handling to the migration script to catch and report any issues during the migration process.

## Implementation Details

### 1. Updated Migration Script

We modified the `migrate_db.py` script to:
- Check for missing columns in existing tables
- Use a table recreation approach for schema changes
- Preserve existing data during migrations
- Handle errors gracefully with proper rollback
- Handle field name discrepancies between frontend and backend

### 2. Field Name Mapping

We identified and addressed discrepancies between frontend and backend field names:

| Table | Backend Field | Frontend Field |
|-------|--------------|----------------|
| SavedImpulse | description | item |
| SavedImpulse | projected_value_1yr | potential_value |

The migration script now handles these discrepancies by:
1. Detecting when tables have inconsistent field names
2. Creating a new table with the correct schema
3. Mapping data from old field names to new field names during migration
4. Preserving all existing data

### 3. API Flexibility

We updated the API endpoints to accept both naming conventions:
- Frontend can send `item` or `description`
- Frontend can send `potential_value` or `projected_value_1yr`
- Backend will correctly handle both naming conventions

### 4. Database Fix Script

We created a `fix_database.sh` script that:
- Backs up the current database
- Runs the migration script
- Initializes the database with the updated schema
- Creates demo users if needed

### 5. Documentation

We added comprehensive documentation:
- Updated the README with information about database migrations
- Created detailed database schema documentation
- Added troubleshooting information for common database errors

## Lessons Learned

1. **SQLite Constraints**: SQLite has limitations when it comes to altering table schemas, particularly with constraints like UNIQUE.

2. **Migration Strategy**: For database schema changes, a table recreation approach is more reliable than trying to alter existing tables.

3. **Backup Importance**: Always create backups before performing database migrations to prevent data loss.

4. **Error Handling**: Comprehensive error handling is essential for database operations to ensure data integrity.

## Future Recommendations

1. **Schema Planning**: Plan the database schema carefully from the beginning to minimize the need for migrations.

2. **Migration Testing**: Test migrations thoroughly in development environments before applying them to production.

3. **Consider ORM Migrations**: For more complex applications, consider using a dedicated ORM migration system like Alembic.

4. **Versioning**: Implement a version tracking system for database schemas to make it easier to identify and apply necessary migrations. 