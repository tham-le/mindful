# MindfulWealth Documentation

Welcome to the MindfulWealth documentation. This directory contains detailed information about the application, its architecture, and guides for troubleshooting common issues.

## Documentation Index

### General Documentation

- [Main README](../README.md) - Overview of the application and setup instructions

### Database Documentation

- [Database Schema](database_schema.md) - Detailed information about the database schema
- [Database Migration Summary](database_migration_summary.md) - Documentation of the migration issue and solution
- [Database Fix Summary](database_fix_summary.md) - Summary of the database fix implementation
- [Database Troubleshooting Guide](database_troubleshooting.md) - Step-by-step guide for resolving database issues
- [Database Improvements](database_improvements.md) - Overview of improvements made to the database migration system

### Troubleshooting

- [Troubleshooting Guide](troubleshooting.md) - Comprehensive guide for resolving common issues
- [Chat Troubleshooting Guide](chat_troubleshooting.md) - Solutions for chat functionality issues

## Application Structure

The MindfulWealth application consists of:

1. **Backend (Flask API)**
   - Located in the `backend` directory
   - Provides authentication and data management
   - Uses SQLite for data storage

2. **Frontend (React)**
   - Located in the `mindfulwealth-react` directory
   - Provides the user interface
   - Communicates with the backend API

3. **Scripts**
   - `setup.sh` - Sets up the application
   - `start.sh` - Starts both frontend and backend
   - `fix_database.sh` - Fixes database issues

## Getting Started

To get started with the application, follow the instructions in the [main README](../README.md).

## Contributing

If you'd like to contribute to the documentation, please follow these guidelines:

1. Use Markdown for all documentation
2. Keep the documentation up to date with code changes
3. Include examples and code snippets where appropriate
4. Link to related documentation where relevant 