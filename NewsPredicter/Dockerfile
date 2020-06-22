FROM python:latest

ADD lib /lib/
ADD conf /conf/
ADD data /data/
ADD launchInitialisation.py /
ADD launchNewsSearchToPred.py /
ADD launchNewsSearchToTrain.py /
ADD launchSendSignal.py /
ADD launchMoulinette.py /
ADD launchUpdatePrices.py /
ADD entry.sh /
ADD crontab.txt /

RUN apt-get update && apt-get install -y cron

RUN pip install sklearn pandas numpy tensorflow nltk yfinance newsapi-python pymongo matplotlib lxml html5lib BeautifulSoup4

RUN chmod 777 /entry.sh
RUN /usr/bin/crontab /crontab.txt