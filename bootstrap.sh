#!/usr/bin/env bash

apt-get update
apt-get install -y python-pip
sudo easy_install supervisor
apt-get install -y build-essential libssl-dev libffi-dev python-dev libffi-dev  libpq-dev redis-server postgresql postgresql-contrib nginx uwsgi
pip install virtualenv
pip install supervisor


#apt-get install -y apache2
#if ! [ -L /var/www ]; then
#  rm -rf /var/www
#  ln -fs /vagrant /var/www
#fi

python2 -m virtualenv /vagrant/.env
/vagrant/.env/bin/pip install -r /vagrant/requirements.txt
/vagrant/.env/bin/python /vagrant/manage.py collectstatic
/usr/bin/python3 -m virtualenv /vagrant/autobahn_proj/.env
/vagrant/autobahn_proj/.env/bin/pip install -r /vagrant/autobahn_proj/requirements.txt
sudo -i -u postgres
sudo psql -f postgre_conf.sql
sudo /etc/supervisord -c /vagrant/supervisord.conf
sudo /etc/init.d/nginx restart

/vagrant/.env/bin/python /vagrant/manage.py makemigrations
/vagrant/.env/bin/python /vagrant/manage.py migrate


