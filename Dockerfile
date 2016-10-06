FROM ubuntu:14.04
MAINTAINER Bogdan Vodopyan <spawnvpn@gmail.com>
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code

RUN apt-get update && apt-get install -y python-pip libcups2-dev build-essential libssl-dev libssh-dev libssh2-1-dev libssh2-1 python-dev python3-dev libffi-dev libpq-dev libxslt1-dev libxml2-dev libz-dev redis-server postgresql postgresql-contrib nginx supervisor && easy_install django-sentry && pip install uwsgi

ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
RUN /usr/bin/python /code/manage.py collectstatic --noinput

#ADD . /final_project_web
#RUN /usr/bin/pip install -r /final_project_web/requirements.txt



