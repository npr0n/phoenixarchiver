#!/bin/bash
echo "setting up environment variables for cron"
printenv > /etc/environment

echo "set up environment for cron."
echo "# crontab -l:"
crontab -l
echo ""
echo "starting cron."
cron -f