#!/bin/bash
printenv > /etc/environment
echo PYTHONPATH=/usr/local/lib/python >> /etc/environment

cron -f