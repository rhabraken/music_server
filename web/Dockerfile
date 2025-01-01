# Use a lightweight Debian-based Python image
FROM python:3.12-slim

# Metadata labels
LABEL description="Docker image for Streamlit app"

# Install required packages
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl \
        nano \
        git \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Streamlit and Requests
RUN pip install streamlit requests

# Copy the Streamlit app script to the container
COPY music_server/web/main.py /app/main.py
WORKDIR /app

# Expose the Streamlit app port
EXPOSE 8501

# Default command to start the Streamlit app
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]
