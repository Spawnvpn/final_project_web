#!/usr/bin/env bash

apt-get update
apt-get install -y python-pip python3-pip
apt-get install -y python-virtualenv libcups2-dev build-essential libssl-dev libssh-dev libssh2-1-dev libssh2-1 libffi-dev python-dev python3-dev libffi-dev libpq-dev libxslt1-dev libxml2-dev libz-dev redis-server postgresql postgresql-contrib nginx
easy_install django-sentry
sudo pip install virtualenv
sudo pip install uwsgi

apt-get install -y supervisor


#apt-get install -y apache2
#if ! [ -L /var/www ]; then
#  rm -rf /var/www
#  ln -fs /vagrant /var/www
#fi

/usr/bin/python2.7 -m virtualenv /vagrant/.env
/vagrant/.env/bin/pip install -r /vagrant/requirements.txt
/vagrant/.env/bin/python2 /vagrant/manage.py collectstatic --noinput
virtualenv --python=/usr/bin/python3.4 /vagrant/autobahn_proj/.env
/vagrant/autobahn_proj/.env/bin/pip install -r /vagrant/autobahn_proj/requirements.txt

export PGPASSWORD='admin'
sudo -E su postgres -c "psql -f /vagrant/postgre_conf.sql"
/vagrant/.env/bin/python /vagrant/manage.py makemigrations
/vagrant/.env/bin/python /vagrant/manage.py migrate
supervisord -c /vagrant/supervisord.conf
source /vagrant/.env/bin/activate
sudo ln -s /vagrant/final_project_web_nginx.conf /etc/nginx/sites-enabled
sudo /etc/init.d/nginx restart


