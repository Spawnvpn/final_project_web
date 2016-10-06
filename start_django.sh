#!/bin/bash

/usr/bin/python manage.py migrate
cd /code/image_aggregator/web_bot
python scrapyd-deploy web_bot
cd /code
uwsgi --ini runtime/final_project_web.ini

