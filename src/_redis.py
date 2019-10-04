import redis
from Constants import env
from Environment import get_env


class _redis():
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        redis_domain = get_env(env.REDIS_DOMAIN)
        redis_password = get_env(env.REDIS_PASSWORD)
        self.redis = redis.StrictRedis(
            redis_domain,
            6379,
            encoding="utf-8",
            decode_responses=True,
            password=redis_password)

    def set(self, name, value):
        self.redis.set(name, value)

    def get(self, name):
        return self.redis.get(name)

    def set_bool(self, name, value: bool):
        if value:
            self.redis.set(name, 1)
        else:
            self.redis.set(name, 0)

    def get_bool(self, name):
        value = int(self.redis.get(name))
        return bool(value)

    def get_run_mode(self):
        run_mode = self.get(env.RUN_MODE)
        if run_mode is None:
            self.set_run_mode_testing()
        run_mode = self.get(env.RUN_MODE)
        return run_mode

    def sadd(self, name, value):
        self.redis.sadd(name, value)

    def smembers(self, name):
        result = self.redis.smembers(name)
        return result

    def lpush(self, name, value):
        self.redis.lpush(name, value)

    def rpush(self, name, value):
        self.redis.rpush(name, value)

    def llen(self, name):
        llen = self.redis.llen(name)

    def get_list(self, name):
        length = self.redis.llen(name)
        list = self.redis.lrange(name, 0, length)
        return list

    def set_run_mode_testing(self):
        self.set(env.RUN_MODE, env.RUN_MODE_TESTING)

    def set_run_mode_live(self):
        self.set(env.RUN_MODE, env.RUN_MODE_LIVE)

    def expire_now(self, name):
        self.redis.expire(name, 0)

    def incr_one(self, name):
        self.redis.incr(name, 1)


if __name__ == "__main__":
    redis = _redis()
    # redis.set_run_mode_live()
    # print(redis.get_run_mode())

    # redis.set_run_mode_testing()
    # print(redis.get_run_mode())

    redis.expire_now("xlog")
    redis.rpush("xlog", "log 1")
    redis.rpush("xlog", "log 1")
    redis.rpush("xlog", "log 2")
    redis.rpush("xlog", "log 2")

    list = redis.get_list("xlog")
    print(list)
    print("done")
