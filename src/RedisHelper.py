import redis
from Constants import env
from Environment import get_env

_redis_domain = get_env(env.REDIS_DOMAIN)
_redis = redis.StrictRedis(_redis_domain, 6379, charset="utf-8", decode_responses=True, password='adminadmin')


class redis_():
    @staticmethod
    def set(key, value):
        _redis.set(key, value)

    @staticmethod
    def get(key):
        return _redis.get(key)

    @staticmethod
    def set_bool(key, value: bool):
        if value:
            _redis.set(key, 1)
        else:
            _redis.set(key, 0)

    @staticmethod
    def get_bool(key):
        value = int(_redis.get(key))
        return bool(value)

    @staticmethod
    def get_run_mode():
        run_mode = redis_.get(env.RUN_MODE)
        if run_mode is None:
            redis_.set_run_mode_testing()
        run_mode = redis_.get(env.RUN_MODE)
        return run_mode

    @staticmethod
    def set_run_mode_testing():
        redis_.set(env.RUN_MODE, env.RUN_MODE_TESTING)

    @staticmethod
    def set_run_mode_live():
        redis_.set(env.RUN_MODE, env.RUN_MODE_LIVE)


if __name__ == "__main__":
    redis_.set_run_mode_live()
    print(redis_.get_run_mode())

    redis_.set_run_mode_testing()
    print(redis_.get_run_mode())
