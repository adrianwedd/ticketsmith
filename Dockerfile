# Base Dockerfile for TICKETSMITH backend
FROM python:3.11-slim

WORKDIR /app

# Install Python dependencies first for better caching
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Default command runs the example CLI
CMD ["python", "-m", "ticketsmith.cli", "Hello"]
