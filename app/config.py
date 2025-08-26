from os import getenv

class Config:
    SECRET_KEY = getenv('SECRET_KEY', 'dev')
    SQLALCHEMY_DATABASE_URI = getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_ENGINE_OPTIONS = {'pool_pre_ping': True}
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = getenv('JWT_SECRET_KEY', 'jwt-dev')
    REDIS_URL = getenv('REDIS_URL', 'redis://localhost:6379/0')
    CELERY_BROKER_URL = getenv('CELERY_BROKER_URL', REDIS_URL)
    CELERY_RESULT_BACKEND = getenv('CELERY_RESULT_BACKEND', REDIS_URL)

    APP_PRUNE_DAYS = int(getenv('APP_PRUNE_DAYS', 30))

class Dev(Config): 
    pass

class Prod(Config): 
    pass