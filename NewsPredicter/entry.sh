#!/bin/sh

# initialisation

/usr/local/bin/python3.8 launchInitialisation.py
/usr/local/bin/python3.8 launchNewsSearch.py
/usr/local/bin/python3.8 launchUpdatePrices.py
/usr/local/bin/python3.8 launchMoulinette.py

# activation crontab
/usr/sbin/crond -f -l 8