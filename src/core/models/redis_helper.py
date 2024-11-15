from redis import Redis
from core.config import settings


class RedisHelper:
    def __init__(
            self,
            url: str):

        self.redis: Redis = Redis.from_url(
            url=str(url), decode_responses=True)

    def get_redis(self) -> Redis:
        return self.redis

    def disconnect_from_redis(self):
        if self.redis:
            self.redis.close()


redis_helper = RedisHelper(
    url=settings.redis.url)
