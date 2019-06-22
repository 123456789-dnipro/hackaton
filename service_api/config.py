import os


class AppConfig:
    DB_NAME = os.getenv('DB_NAME', 'chats')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_USER = os.getenv('DB_USER', 'gosha')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '1234')
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = os.getenv('REDIS_PORT', '6379')
    REDIS_USER = os.getenv('REDIS_USER', 'user')
    REDIS_PASSWORD = os.getenv('REDIS_PORT', 'pass')


class DevConfig(AppConfig):
    DEBUG = True
