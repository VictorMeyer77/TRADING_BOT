#!/bin/sh

# initialisation

PYTHONHASHSEED=0 python3 launchInitialisation.py
PYTHONHASHSEED=0 python3 launchUpdatePrices.py
PYTHONHASHSEED=0 python3 launchMoulinette.py

# ajout crontab
/usr/bin/crontab /crontab.txt
service cron start

# laisse le conteneur actif
tail -F null