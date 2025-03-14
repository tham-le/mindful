# MindfulWealth Deployment Guide

This document provides instructions for deploying the MindfulWealth application in a production environment.

## Prerequisites

- Docker and Docker Compose installed
- A valid Gemini API key from [Google AI Studio](https://ai.google.dev/)
- Ports 80, 3000, and 5000 available on the host machine

## Quick Deployment

For a quick deployment with all default settings, simply run:

```bash
./deploy.sh
```

This script will:

1. Check for required dependencies
2. Verify port availability
3. Create and configure environment files if needed
4. Validate the Gemini API key
5. Build and start the Docker containers
6. Verify the deployment

## Manual Deployment

If you prefer to deploy manually, follow these steps:

### 1. Configure Environment Files

Create the necessary environment files:

```bash
# Root .env file (for Docker Compose)
cp .env.example .env

# Backend .env file
cp backend/.env.example backend/.env

# Frontend .env file
cp mindfulwealth-react/.env.example mindfulwealth-react/.env.production
```

Edit these files to set your configuration values, especially:

- `GEMINI_API_KEY` in `backend/.env`
- `JWT_SECRET_KEY` in `backend/.env`
- `REACT_APP_API_URL` in `mindfulwealth-react/.env.production`

### 2. Build and Start Containers

```bash
docker-compose build
docker-compose up -d
```

### 3. Verify Deployment

Check if the containers are running:

```bash
docker-compose ps
```

Access the application:

- Frontend: <http://localhost> or <http://localhost:3000>
- Backend API: <http://localhost:5000/api>

## Port Configuration

The application uses the following ports:

- **Port 80**: Main frontend access
- **Port 3000**: Alternative frontend access
- **Port 5000**: Backend API

If any of these ports are already in use on your system, you can modify the port mappings in the `docker-compose.yml` file:

```yaml
services:
  backend:
    ports:
      - "YOUR_CUSTOM_PORT:5000"
  
  frontend:
    ports:
      - "YOUR_CUSTOM_PORT:80"
```

Remember to update the `CORS_ORIGINS` in `backend/.env` and `REACT_APP_API_URL` in `mindfulwealth-react/.env.production` to match your custom ports.

## Development Environment

For local development, use the development script:

```bash
./dev.sh
```

This script allows you to start:

1. Backend only
2. Frontend only
3. Both backend and frontend

## Troubleshooting

### Container Issues

If containers fail to start, check the logs:

```bash
docker-compose logs
```

### API Connection Issues

If the frontend cannot connect to the backend:

1. Verify that the backend container is running
2. Check that `REACT_APP_API_URL` in the frontend environment is correct
3. Ensure that `CORS_ORIGINS` in the backend environment includes your frontend URL

### Gemini API Issues

If the chat functionality is not working:

1. Verify your Gemini API key is valid
2. Check the backend logs for API-related errors
3. Ensure the backend can reach the Gemini API (internet connectivity)

## Maintenance

### Updating the Application

To update the application:

```bash
git pull
./deploy.sh
```

### Backing Up Data

The application data is stored in `backend/mindfulwealth.db`. To back up this file:

```bash
cp backend/mindfulwealth.db backend/mindfulwealth.db.backup
```

### Monitoring

Monitor the application logs:

```bash
docker-compose logs -f
```

## Security Considerations

For a production deployment, consider:

1. Using HTTPS with a proper SSL certificate
2. Setting a strong `JWT_SECRET_KEY` in `backend/.env`
3. Restricting access to the backend API
4. Implementing proper authentication and authorization
5. Regular security updates for all components

## Support

If you encounter any issues with deployment, please:

1. Check the troubleshooting section above
2. Review the application logs
3. Consult the [Chat Fixes documentation](CHAT_FIXES.md) for specific chat functionality issues
4. Contact the development team for further assistance
