FROM python:3
WORKDIR /app

RUN apt-get update && apt-get install -y cron
RUN wget https://mega.nz/linux/repo/Debian_11/amd64/megacmd-Debian_11_amd64.deb \
 && apt-get install ./megacmd-Debian_11_amd64.deb -y \
 && rm ./megacmd-Debian_11_amd64.deb

COPY * /app
RUN python3 -m venv /app/venv
RUN /app/venv/bin/python3 -m pip install --no-cache-dir -r /app/requirements.txt

COPY crontab /etc/cron.d/crontab
RUN chmod 0644 /etc/cron.d/crontab
RUN /usr/bin/crontab /etc/cron.d/crontab
RUN chmod +x /app/entrypoint.sh

# run crond as main process of container
ENTRYPOINT [ "/app/entrypoint.sh" ]
