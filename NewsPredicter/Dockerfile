FROM debian:buster

ADD lib /lib/
ADD conf /conf/
ADD data /data/
ADD launchInitialisation.py /
ADD launchNewsSearchToTrain.py /
ADD launchNewsSearchToPred.py /
ADD launchSendSignal.py /
ADD launchMoulinette.py /
ADD launchUpdatePrices.py /
ADD entry.sh /
ADD crontab.txt /


RUN dpkg --add-architecture armhf && dpkg --add-architecture arm64 \
    && apt-get update && apt-get install -y \
        openjdk-11-jdk automake autoconf libpng-dev \
        curl zip unzip libtool swig zlib1g-dev pkg-config git wget xz-utils \
        python3-numpy python3-pip python3-mock \
        libpython3-dev libpython3-all-dev \
        libpython3-dev:armhf libpython3-all-dev:armhf \
        libpython3-dev:arm64 libpython3-all-dev:arm64 g++ gcc \
        gfortran libatlas-base-dev libopenblas-dev liblapack-dev libxml2-dev libxslt-dev \
        libhdf5-dev libc-ares-dev libeigen3-dev libblas-dev cython cron python-h5py

RUN wget https://github.com/Qengineering/Tensorflow-Raspberry-Pi/raw/master/tensorflow-2.1.0-cp37-cp37m-linux_armv7l.whl

RUN pip3 install firebase-admin scikit-learn --index-url https://piwheels.org/simple
RUN pip3 install pandas nltk yfinance newsapi-python pymongo lxml html5lib BeautifulSoup4
RUN pip3 install pybind11 numpy
RUN pip3 install --upgrade setuptools
RUN pip3 install tensorflow-2.1.0-cp37-cp37m-linux_armv7l.whl

