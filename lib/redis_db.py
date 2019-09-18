from config import config_info
import redis


class RedisInstance:
    @staticmethod
    def instance():
        if not hasattr(RedisInstance, "_instance"):
            # New instance
            RedisInstance._instance = RedisInstance()
        return RedisInstance._instance

    def __init__(self):
        self.config = config_info['REDIS']
        self.redis = self.redis_db()

    def redis_db(self):
        redis_db = redis.StrictRedis(
            host=self.config['host'],
            port=self.config['port'],
            db=self.config['db'],
            password=self.config['password']
        )
        return redis_db
