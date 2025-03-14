# Port Compatibility

This document outlines the port configuration for the MindfulWealth application and how to handle port conflicts.

## Default Port Configuration

The MindfulWealth application uses the following ports by default:

- **Port 80**: Main frontend access (Nginx)
- **Port 3000**: Alternative frontend access (mapped to port 80 inside the container)
- **Port 5000**: Backend API (Flask)

## Port Conflict Detection

The deployment script (`deploy.sh`) automatically checks for port conflicts before starting the application. If a conflict is detected:

1. For ports 80 and 5000, the script will abort and display information about the conflicting process.
2. For port 3000, the script will display a warning but continue, as the application will still be accessible on port 80.

## Changing Port Configuration

If you need to use different ports, you can modify the configuration in several places:

### 1. Docker Compose Configuration

Edit the `docker-compose.yml` file to change the port mappings:

```yaml
services:
  backend:
    ports:
      - "YOUR_CUSTOM_BACKEND_PORT:5000"
  
  frontend:
    ports:
      - "YOUR_CUSTOM_FRONTEND_PORT:80"
      - "YOUR_CUSTOM_ALT_PORT:80"
```

### 2. Environment Variables

Update the following environment files to match your custom ports:

- In `backend/.env`:

  ```
  PORT=5000  # This is the internal port, usually no need to change
  CORS_ORIGINS=http://localhost:YOUR_CUSTOM_FRONTEND_PORT,http://localhost:YOUR_CUSTOM_ALT_PORT
  ```

- In `mindfulwealth-react/.env.production`:

  ```
  REACT_APP_API_URL=http://localhost:YOUR_CUSTOM_BACKEND_PORT/api
  ```

### 3. Nginx Configuration

If you change the frontend port, you may need to update the Nginx configuration in `mindfulwealth-react/nginx.conf`:

```
server {
    listen YOUR_CUSTOM_FRONTEND_PORT;
    # ... rest of the configuration
}
```

## Development Environment

For the development environment, the `dev.sh` script also checks for port conflicts on ports 5000 (backend) and 3000 (frontend). If conflicts are detected, the script will abort and display information about the conflicting processes.

## Common Port Conflicts

Common applications that might conflict with MindfulWealth ports:

- **Port 80**: Web servers (Apache, Nginx), other web applications
- **Port 3000**: Node.js applications, development servers
- **Port 5000**: Python web applications, development servers

## Troubleshooting

If you encounter port conflicts:

1. Identify the process using the conflicting port:

   ```bash
   lsof -i:PORT_NUMBER
   ```

2. Stop the conflicting process or choose a different port for MindfulWealth.

3. If you choose a different port, update all the configuration files as described above.

## Security Considerations

When changing ports, consider the following security implications:

- Ports below 1024 typically require root/administrator privileges
- Some firewalls may block non-standard ports
- If exposing the application to the internet, ensure proper security measures are in place

## Recommended Production Configuration

For production environments, we recommend:

- Using port 80 for HTTP access (or port 443 for HTTPS)
- Not exposing the backend API port (5000) directly to the internet
- Using a reverse proxy to handle SSL termination and routing
