# Base image with Python and FFmpeg
FROM python:3.10-slim

# Install system dependencies + FFmpeg with all codecs
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    ffmpeg \
    libavcodec-extra \
    libssl-dev && \
    rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app.py \
    FLASK_ENV=production

# Create and set working directory
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files
COPY . .

# Cleanup
RUN find . -type d -name "__pycache__" -exec rm -rf {} + && \
    find . -type f -name "*.py[co]" -delete

# Expose port
EXPOSE 80

# Run with Gunicorn (production-ready)
CMD ["gunicorn", "--bind", "0.0.0.0:80", "--workers", "4", "app:app"]