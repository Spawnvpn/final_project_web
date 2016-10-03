## Image Aggregator

This is a simple application for searching images via Google, Yandex and Instagram. Based on Django and works with: redis, scrapyd, autobahn.

## Installation

First you need clone project from https://github.com/Spawnvpn/final_project_web.git

After in the root of the project to create a virtual environment (in your project root: `virtualenv -p python2.7 .env`) and execute following command:<br>
```
. .env/bin/activate
pip install -r requirements.txt
export PGPASSWORD='admin'
sudo -E su postgres -c "psql -f postgre_conf.sql"
python manage.py makemigrations && python manage.py migrate
python manage.py runserver
```

After in new terminal:<br>
```
cd .../final_project_web/autobahn_proj
virtualenv -p python3 .env
. .env/bin/activate
pip install -r requirements
python server.py
```

After in new terminal:<br>
```
cd .../final_project_web
. .env/bin/activate
scrapyd
```

After in new terminal:<br>
```
cd .../final_project_web
. .env/bin/activate
cd image_aggregator/web_bot
scrapyd-deploy web_bot
```

After in new terminal:
```
redis-server
or run your redis-server as daemon
```


## Use
```
In your browser: localhost:8000
```

## Also

You may deploy this application to vagrant box.<br>
To do this:<br>
```
sudo apt-get install virtualbox
sudo apt-get install vagrant
```
In project directory: `vagrant up --provision`<br>
The project will be deployed on a virtual machine and start the nginx server. For use enter in your browser: `http://127.0.0.1:5678`
