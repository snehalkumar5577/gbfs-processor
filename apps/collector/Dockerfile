
# Use the official Python image
FROM python:3.9-slim

# Set environment variables to avoid Python buffering
ENV PYTHONUNBUFFERED=1

# Set up working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the collector code into the container
COPY . .

# Specify python path
ENV PYTHONPATH=/app

# Command to run the collector script
CMD ["python", "collector/collector.py"]
