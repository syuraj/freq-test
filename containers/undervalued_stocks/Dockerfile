# Use official Python image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    cron \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the script and any needed files
COPY under-valued.py .
COPY finviz_midcap_tech.csv .

# Add crontab file and entry
RUN echo "0 2 * * * python /app/under-valued.py >> /app/cron.log 2>&1" > /etc/cron.d/under-valued-cron
RUN chmod 0644 /etc/cron.d/under-valued-cron
RUN crontab /etc/cron.d/under-valued-cron

# Create the log file to be able to run tail
RUN touch /app/cron.log

# Run the command on container startup
CMD ["cron", "-f"]