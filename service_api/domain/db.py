import asyncpg
import asyncpgsa
from asyncpgsa import pg
from sanic import Sanic
from sqlalchemy.schema import CreateTable

from service_api.domain.models import models


async def init_db(app: Sanic, db_prefix=''):
    db_creds = {
        'user': app.config.DB_USER,
        'password': app.config.DB_PASSWORD,
        'host': app.config.DB_HOST,
        'port': app.config.DB_PORT,
        'database': 'postgres'
    }
    conn = await asyncpg.connect(**db_creds)
    query = f"CREATE DATABASE {app.config.DB_NAME}{'_' if db_prefix else ''}{db_prefix} OWNER {db_creds['user']};"
    await conn.fetchrow(query)
    await conn.close()
    pool = await get_pool()
    async with pool.acquire() as conn:
        for table in models:
            create_expr = CreateTable(table)
            await conn.execute(create_expr)


async def get_pool():
    from service_api.app import app
    pool = app.pool if hasattr(app, 'pool') else None
    if not pool:
        db_creds ={
            'user': app.config.DB_USER,
            'password': app.config.DB_PASSWORD,
            'host': app.config.DB_HOST,
            'port': app.config.DB_PORT,
            'database': app.config.DB_NAME,
        }
        # await pg.init(db_creds)
        pool = await asyncpgsa.create_pool(**db_creds)
    return pool
