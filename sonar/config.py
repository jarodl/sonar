from datetime import timedelta

CELERY_RESULT_BACKEND = "redis"
CELERY_REDIS_HOST = "localhost"
CELERY_REDIS_PORT = 6379
CELERY_REDIS_DB = 0
CELERYBEAT_SCHEDULE = {
    "runs-every-30-seconds": {
        "task": "sonar.update",
        "schedule": timedelta(seconds=30)
    },
}

BROKER_URL = 'redis://localhost:6379/0'

SECRET_KEY = '=\xce\xc4\xd1Ud\xd3\xd4\xa8M\xf0\x17\x98^H)=\xb7d:\xa2wco',
DEBUG = True

