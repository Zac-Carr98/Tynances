FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-tk \
    && apt-get clean

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the .env file
COPY .env /app/.env

# Command
CMD ["python", "main.py"]
