FROM python:3
WORKDIR /app
COPY * /app
COPY crontab /etc/cron.d/crontab
RUN pip install --no-cache-dir -r requirements.txt --target=/usr/local/lib/python
RUN apt-get update && apt-get install -y cron
RUN chmod 0644 /etc/cron.d/crontab
RUN /usr/bin/crontab /etc/cron.d/crontab
RUN chmod +x /app/entrypoint.sh

# run crond as main process of container
ENTRYPOINT [ "/app/entrypoint.sh" ]
