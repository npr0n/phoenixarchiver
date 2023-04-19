FROM python:3
RUN apt-get update && apt-get install -y cron
RUN wget https://mega.nz/linux/repo/Debian_11/amd64/megacmd-Debian_11_amd64.deb \
 && apt-get install ./megacmd-Debian_11_amd64.deb -y \
 && rm ./megacmd-Debian_11_amd64.deb
COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh

# run crond as main process of container
ENTRYPOINT [ "/entrypoint.sh" ]
