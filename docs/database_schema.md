# MindfulWealth Database Schema

This document provides a detailed overview of the database schema used in the MindfulWealth application.

## Overview

MindfulWealth uses SQLite as its database engine. The database file is located at `backend/mindfulwealth.db`.

## Tables

### Users

The `users` table stores user information and authentication details.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Unique identifier for the user |
| name | TEXT | NOT NULL | User's display name |
| email | TEXT | UNIQUE | User's email address (used for login) |
| password_hash | TEXT | | Hashed password for authentication |
| is_demo | BOOLEAN | DEFAULT 0 | Flag indicating if this is a demo user |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | When the user account was created |
| last_login | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | When the user last logged in |

### Transactions

The `transactions` table records financial transactions.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Unique identifier for the transaction |
| user_id | INTEGER | FOREIGN KEY | Reference to the users table |
| amount | FLOAT | NOT NULL | Transaction amount |
| category | TEXT | NOT NULL | Transaction category |
| description | TEXT | | Optional description of the transaction |
| date | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | When the transaction occurred |
| is_expense | BOOLEAN | DEFAULT 1 | Whether this is an expense (1) or income (0) |

### Budgets

The `budgets` table stores budget information by category.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Unique identifier for the budget |
| user_id | INTEGER | FOREIGN KEY | Reference to the users table |
| category | TEXT | NOT NULL | Budget category |
| amount | FLOAT | NOT NULL | Budget amount |
| period | TEXT | DEFAULT 'monthly' | Budget period (e.g., 'monthly', 'weekly') |

### SavedImpulses

The `saved_impulses` table tracks redirected impulse purchases.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Unique identifier for the saved impulse |
| user_id | INTEGER | FOREIGN KEY | Reference to the users table |
| description | TEXT | NOT NULL | Description of the item not purchased |
| amount | FLOAT | NOT NULL | Amount saved by not making the purchase |
| category | TEXT | | Category of the saved impulse |
| date | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | When the impulse was saved |
| projected_value_1yr | FLOAT | NOT NULL | Projected value after 1 year |
| projected_value_5yr | FLOAT | NOT NULL | Projected value after 5 years |

#### Field Name Mappings

For compatibility between frontend and backend, some field names are mapped:

| Database Field | Frontend Field | Description |
|----------------|---------------|-------------|
| description | item | Description of the saved impulse |
| projected_value_1yr | potential_value | Projected value after 1 year |

The API handles these mappings automatically, so you can use either naming convention when sending data to the API.

## Relationships

- Each user can have multiple transactions (one-to-many)
- Each user can have multiple budgets (one-to-many)
- Each user can have multiple saved impulses (one-to-many)

## Migrations

Database migrations are handled by the `migrate_db.py` script. This script:

1. Checks for missing tables and creates them
2. Checks for missing columns in existing tables
3. Updates the schema while preserving existing data

When significant schema changes are needed, the migration script:
1. Creates a backup of the current database
2. Creates a new table with the updated schema
3. Copies data from the old table to the new one
4. Drops the old table
5. Renames the new table to the original name

## Backup System

Before any migration, the current database is backed up to `mindfulwealth.db.backup`. This ensures that data can be recovered if a migration fails. 