import redis.asyncio as redis 
from app.core.config import get_settings

settings = get_settings()

# Singleton Redis connection
async def get_redis():
    if not hasattr(get_redis, "redis"):
        get_redis.redis = redis.from_url(
            settings.REDIS_URL or "redis://localhost",
            decode_responses=True  # optional: ensures strings instead of bytes
        )
    return get_redis.redis

async def add_to_blacklist(jti: str, exp: int):
    """Add a token's JTI to the blacklist"""
    redis_conn = await get_redis()
    await redis_conn.set(f"blacklist:{jti}", "1", ex=exp)

async def is_blacklisted(jti: str) -> bool:
    """Check if a token's JTI is blacklisted"""
    redis_conn = await get_redis()
    return bool(await redis_conn.exists(f"blacklist:{jti}"))
