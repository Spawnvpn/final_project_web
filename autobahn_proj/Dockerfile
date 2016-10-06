FROM ubuntu:14.04
MAINTAINER Bogdan Vodopyan <spawnvpn@gmail.com>
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code

RUN apt-get update && apt-get install -y python3-pip build-essential python-dev python3-dev redis-server postgresql postgresql-contrib libpq-dev
ADD requirements.txt /code/
RUN pip3 install -r requirements.txt
ADD . /code/

#ADD . /autobahn_proj
#RUN /usr/bin/pip3 install -r /final_project_web/requirements.txt

