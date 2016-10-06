import os
DB_CONN = "host='postgres' dbname='final_project_web' user='admin' password='admin'"

RAVEN_URL = 'https://8ff8d6c9c1e2413eb517774e481074c1:4a819bdfaa644649978440d6ee752545@sentry.io/97142'

# REDIS_CON = 'redis://localhost:8000/redis/0'

REDIS_CON = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
