# Use the official Python image.
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend code into the container
COPY . .

# Copy the .env file from the parent directory into the container
COPY .env .env

ENV DEV=0

# Expose the port the app runs on
EXPOSE 8080

# Start the Flask application
CMD ["python", "app.py"]