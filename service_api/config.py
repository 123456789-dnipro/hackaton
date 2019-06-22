import os


class AppConfig:
    DB_NAME = os.getenv('DB_NAME', 'parking')
    DB_HOST = os.getenv('DATABASE_URL', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_USER = os.getenv('DB_USER', 'su_admin')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'pass')
    REDIS_HOST = os.getenv('REDIS_URL', 'localhost')
    REDIS_PORT = os.getenv('REDIS_PORT', '6379')
    REDIS_USER = os.getenv('REDIS_USER', 'user')
    REDIS_PASSWORD = os.getenv('REDIS_PORT', 'pass')


class DevConfig(AppConfig):
    DEBUG = True
