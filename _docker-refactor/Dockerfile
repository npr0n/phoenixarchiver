FROM python:3
WORKDIR /app
RUN apt-get update && apt-get install -y cron
RUN wget https://mega.nz/linux/repo/Debian_11/amd64/megacmd-Debian_11_amd64.deb \
 && apt-get install ./megacmd-Debian_11_amd64.deb -y \
 && rm ./megacmd-Debian_11_amd64.deb
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --target=/usr/local/lib/python
COPY * /app
COPY crontab /etc/cron.d/crontab
RUN chmod 0644 /etc/cron.d/crontab
RUN /usr/bin/crontab /etc/cron.d/crontab
RUN chmod +x /app/entrypoint.sh

# run crond as main process of container
ENTRYPOINT [ "/app/entrypoint.sh" ]
