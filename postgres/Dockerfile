FROM python:3.11-slim

# Set working directory
WORKDIR /scripts

# Copy the local script into the container
COPY dbinit.py .
COPY requirements.txt .
COPY .env .env
ENV DEV=0
# Install required packages (if any)
RUN pip install -r requirements.txt

# Command to run the script
ENTRYPOINT ["python", "dbinit.py"]