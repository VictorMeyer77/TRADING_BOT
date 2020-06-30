FROM python:alpine

ADD conf /conf
ADD lib /lib
ADD main.py /

RUN pip3 install cherrypy pymongo

RUN apk add --no-cache tzdata
RUN ln -snf /usr/share/zoneinfo/Europe/Paris /etc/localtime && echo Europe/Paris > /etc/timezone