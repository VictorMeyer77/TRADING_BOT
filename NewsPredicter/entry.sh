#!/bin/sh

# initialisation

PYTHONHASHSEED=0 /usr/local/bin/python3.8 launchInitialisation.py
PYTHONHASHSEED=0 /usr/local/bin/python3.8 launchUpdatePrices.py
PYTHONHASHSEED=0 /usr/local/bin/python3.8 launchMoulinette.py

# activation crontab
/usr/sbin/crond -f -l 8