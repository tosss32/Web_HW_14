
from fastapi import Depends
from fastapi_ratelimit import rate_limit
from redis_pool import create_redis_pool


async def get_limit():
    global redis_pool  
    redis_pool = await create_redis_pool()
    limit = rate_limit(5, 60, key_func=lambda x: x['client'].host, redis_pool=redis_pool)
    return limit