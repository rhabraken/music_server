# Use a lightweight Debian-based Python image
FROM python:3.12-slim

# Metadata labels
LABEL description="Docker image with Python, Streamrip, and an API server"

# Install required packages
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl \
        nano \
        git \
        iproute2 \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install streamrip, Flask, Gunicorn, and Flask-Cors
RUN pip install git+https://github.com/ralmachado/streamrip.git requests flask gunicorn flask-cors

# Create and set permissions for /root/.config
RUN mkdir -p /root/.config && \
    chown 1000:1000 /root/.config && \
    chmod 755 /root/.config

# Add the API server script to the container
COPY music_server/api/main.py /app/main.py
WORKDIR /app

# Expose the API server port
EXPOSE 5000

# Default command to start the API server with Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "main:app"]
