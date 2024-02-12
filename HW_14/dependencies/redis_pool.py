"""
Модуль для створення redis_pool.

Містить функції для створення redis_pool.
"""
import aioredis

async def create_redis_pool():
    
    redis_address = ('localhost', 6379)
    redis_password = None

    pool = await aioredis.create_redis_pool(
        address=redis_address,
        password=redis_password,
        minsize=5,
        maxsize=10,
    )
    
    return pool