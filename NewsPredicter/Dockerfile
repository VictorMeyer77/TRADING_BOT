FROM python:latest

ADD lib /lib/
ADD conf /conf/
ADD data /data/
ADD launchInitialisation.py /
ADD launchNewsSearch.py /
ADD launchTradeNews.py /
ADD launchMoulinette.py /
ADD launchUpdatePrices.py /
ADD entry.sh /
ADD crontab.txt /

RUN apt-get update && apt-get install -y cron

RUN pip install sklearn pandas numpy tensorflow nltk yfinance newsapi-python pymongo matplotlib lxml html5lib BeautifulSoup4

RUN chmod 777 /entry.sh
RUN /usr/bin/crontab /crontab.txt