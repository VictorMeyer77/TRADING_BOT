#!/bin/sh

# initialisation

PYTHONHASHSEED=0 python3 launchInitialisation.py
PYTHONHASHSEED=0 python3 launchUpdatePrices.py
PYTHONHASHSEED=0 python3 launchMoulinette.py

/bin/sh