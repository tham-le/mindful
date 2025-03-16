FROM python:3.10-slim

WORKDIR /app

# Copy only requirements file first to leverage build cache
COPY requirements.txt .

# Install Python dependencies using build cache
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

# Install system dependencies
RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy the rest of the application
COPY . .

# Set environment variables
ENV FLASK_APP=app.py \
    FLASK_ENV=production \
    FLASK_DEBUG=0 \
    PORT=5000 \
    HOST=0.0.0.0

# Expose port
EXPOSE 5000

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
