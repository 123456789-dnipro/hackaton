import os


class AppConfig:
    DB_NAME = os.getenv('DB_NAME')
    DB_HOST = os.getenv('DATABASE_URL', 'localhost')
    DB_PORT = os.getenv('DB_PORT')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    REDIS_HOST = os.getenv('REDIS_URL', 'localhost')


class DevConfig(AppConfig):
    DEBUG = True
