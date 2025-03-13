# MindfulWealth Troubleshooting Guide

This guide provides solutions for common issues you might encounter when setting up or running the MindfulWealth application.

## Setup Issues

### Python Virtual Environment Issues

#### Issue: python3-venv not installed

**Error Message:**
```
Error: The virtual environment was not created successfully because ensurepip is not available.
```

**Solution:**
```bash
sudo apt install python3-venv
```

#### Issue: Virtual environment creation fails

**Solution:**
```bash
rm -rf backend/venv
./setup.sh
```

#### Issue: "externally-managed-environment" errors

**Error Message:**
```
error: externally-managed-environment
```

**Cause:** Your system Python is managed by the OS package manager.

**Solution:** The setup script will automatically create a virtual environment to avoid this issue. If you're running commands manually, make sure to activate the virtual environment:
```bash
cd backend
source venv/bin/activate
```

### Dependency Issues

#### Issue: Backend dependencies not installed

**Solution:**
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

#### Issue: Frontend dependencies not installed

**Solution:**
```bash
cd mindfulwealth-react
npm install
```

## Database Issues

For database-specific issues, please refer to the [Database Troubleshooting Guide](database_troubleshooting.md).

## Application Startup Issues

### Issue: Backend fails to start

**Common causes:**
- Port 5000 is already in use
- Database issues
- Missing dependencies

**Solutions:**
1. Check if another process is using port 5000:
   ```bash
   lsof -i :5000
   ```
   If a process is found, terminate it or change the port in `backend/run.py`.

2. Check for database issues:
   ```bash
   ./fix_database.sh
   ```

3. Verify all dependencies are installed:
   ```bash
   cd backend
   source venv/bin/activate
   pip install -r requirements.txt
   ```

### Issue: Frontend fails to start

**Common causes:**
- Port 3000 is already in use
- Missing dependencies
- Node.js version incompatibility

**Solutions:**
1. Check if another process is using port 3000:
   ```bash
   lsof -i :3000
   ```
   If a process is found, terminate it or change the port in `mindfulwealth-react/package.json`.

2. Verify all dependencies are installed:
   ```bash
   cd mindfulwealth-react
   npm install
   ```

3. Check your Node.js version:
   ```bash
   node --version
   ```
   The application requires Node.js version 14 or higher.

## Authentication Issues

### Issue: Login fails

**Common causes:**
- Incorrect email or password
- Database issues
- Backend not running

**Solutions:**
1. Verify you're using the correct credentials:
   - Default admin: admin@example.com / password
   - Default demo user: Check the console output when running `init_db.py`

2. Check if the backend is running:
   ```bash
   ps aux | grep run.py
   ```

3. Fix database issues:
   ```bash
   ./fix_database.sh
   ```

## Application Performance Issues

### Issue: Slow application performance

**Solutions:**
1. Check your system resources:
   ```bash
   top
   ```

2. Restart the application:
   ```bash
   ./start.sh
   ```

## Getting Help

If you continue to experience issues after trying these solutions, please:

1. Check the application logs for more detailed error messages
2. Refer to the documentation in the `docs` directory
3. Create an issue in the project repository with detailed information about the problem 