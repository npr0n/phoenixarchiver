#!/bin/bash
printenv > /etc/environment
echo PYTHONPATH=/usr/local/lib/python >> /etc/environment

echo "set up environment for cron."
echo "# crontab -l:"
crontab -l

echo "starting cron."
cron -f