#!/bin/bash
if [ -f /app/.env ]
then
  source /app/.env
fi

echo "setting up environment variables for cron"
printenv > /etc/environment
echo PYTHONPATH=/usr/local/lib/python >> /etc/environment
echo ""
cat /etc/environment


echo "set up environment for cron."
echo "# crontab -l:"
crontab -l
echo ""
echo "starting cron."
cron -f