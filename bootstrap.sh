#!/usr/bin/env bash

apt-get update
apt-get install -y python-pip
apt-get install -y build-essential libssl-dev libffi-dev python-dev libffi-dev  libpq-dev redis server
pip install virtualenv

#apt-get install -y apache2
#if ! [ -L /var/www ]; then
#  rm -rf /var/www
#  ln -fs /vagrant /var/www
#fi

python2 -m virtualenv /vagrant/.env
/vagrant/.env/bin/pip install -r /vagrant/requirements.txt
#/vagrant/.env/bin/python /vagrant/manage.py makemigrations
#/vagrant/.env/bin/python /vagrant/manage.py migrate


