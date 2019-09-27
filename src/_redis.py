import redis
from Constants import env
from Environment import get_env


class _redis():
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        redis_domain = get_env(env.REDIS_DOMAIN)
        self.client = redis.StrictRedis(redis_domain, 6379, charset="utf-8", decode_responses=True, password='adminadmin')

    def set(self, key, value):
        self.client.set(key, value)

    def get(self, key):
        return self.client.get(key)

    def set_bool(self, key, value: bool):
        if value:
            self.client.set(key, 1)
        else:
            self.client.set(key, 0)

    def get_bool(self, key):
        value = int(self.client.get(key))
        return bool(value)

    def get_run_mode(self):
        run_mode = self.get(env.RUN_MODE)
        if run_mode is None:
            self.set_run_mode_testing()
        run_mode = self.get(env.RUN_MODE)
        return run_mode

    def set_run_mode_testing(self):
        self.set(env.RUN_MODE, env.RUN_MODE_TESTING)

    def set_run_mode_live(self):
        self.set(env.RUN_MODE, env.RUN_MODE_LIVE)


if __name__ == "__main__":
    redis = _redis()
    redis.set_run_mode_live()
    print(redis.get_run_mode())

    redis.set_run_mode_testing()
    print(redis.get_run_mode())
