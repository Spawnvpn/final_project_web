## Image Aggregator

This is a simple application for searching images via Google, Yandex and Instagram. Based on Django and works with: redis, scrapyd, autobahn.

## Installation

First you need clone project from https://github.com/Spawnvpn/final_project_web.git

After in the root of the project to create a virtual environment (in your project root: virtualenv -p python2.7 .env) and execute following command:<br>
    . .env/bin/activate<br>
    pip install -r requirements.txt<br>
    python manage.py makemigrations && python manage.py migrate<br>
    python manage.py runserver<br>

After in new terminal:<br>
    cd .../final_project_web/autobahn_proj<br>
    virtualenv -p python3 .env<br>
    . .env/bin/activate<br>
    pip install -r requirements<br>
    python server.py<br>

After in new terminal:<br>
    cd .../final_project_web<br>
    . .env/bin/activate<br>
    scrapyd<br>

Configure your DB_PATH in .../final_project_web/image_aggregator/web_bot/web_bot/settings.py and .../final_project_web/autobahn_proj/settings.py.<br>

After in new terminal:<br>
    cd .../final_project_web<br>
    . .env/bin/activate<br>
    cd image_aggregator/web_bot<br>
    scrapyd-deploy web_bot<br>

After in new terminal:
    redis-server<br>
    or run your redis-server as daemon<br>


## Use

In your browser: localhost:8000