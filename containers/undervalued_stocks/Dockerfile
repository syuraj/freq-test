FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    cron \
    && rm -rf /var/lib/apt/lists/*

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

RUN echo "0 12 * * * python /app/under-valued.py >> /app/cron.log 2>&1" > /etc/cron.d/under-valued-cron
RUN chmod 0644 /etc/cron.d/under-valued-cron
RUN crontab /etc/cron.d/under-valued-cron

RUN touch /app/cron.log

CMD ["cron", "-f"]