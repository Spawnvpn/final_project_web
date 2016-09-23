## Image Aggregator

This is a simple application for searching images via Google, Yandex and Instagram. Based on Django and works with: redis, scrapyd, autobahn.

## Installation

First you need clone project from https://github.com/Spawnvpn/final_project_web.git

After in the root of the project to create a virtual environment (in your project root: virtualenv -p python2.7 .env) and execute following command:__
    . .env/bin/activate__
    pip install -r requirements.txt__
    python manage.py makemigrations && python manage.py migrate__
    python manage.py runserver__

After in new terminal:__
    cd .../final_project_web/autobahn_proj__
    virtualenv -p python3 .env__
    . .env/bin/activate__
    pip install -r requirements__
    python server.py__

After in new terminal:__
    cd .../final_project_web__
    . .env/bin/activate__
    scrapyd__

After in new terminal:__
    cd .../final_project_web__
    . .env/bin/activate__
    cd image_aggregator/web_bot__
    scrapyd-deploy web_bot__

After in new terminal:
    redis-server__
    or run your redis-server as daemon__


## Use

In your browser: localhost:8000