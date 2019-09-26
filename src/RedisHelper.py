import redis
from Constants import cons
from Environment import env

redis_domain = env.get(cons.REDIS_DOMAIN)
red = redis.StrictRedis(redis_domain, 6379, charset="utf-8", decode_responses=True, password='adminadmin')


class redis_helper():
    @staticmethod
    def set(key, value):
        red.set(key, value)

    @staticmethod
    def get(key):
        return red.get(key)

    @staticmethod
    def set_bool(key, value: bool):
        if value:
            red.set(key, 1)
        else:
            red.set(key, 0)

    @staticmethod
    def get_bool(key):
        value = int(red.get(key))
        return bool(value)

    @staticmethod
    def get_run_mode():
        run_mode = redis_helper.get(cons.RUN_MODE)
        if run_mode is None:
            redis_helper.set_run_mode_testing()
        run_mode = redis_helper.get(cons.RUN_MODE)
        return run_mode

    @staticmethod
    def set_run_mode_testing():
        redis_helper.set(cons.RUN_MODE, cons.RUN_MODE_TESTING)

    @staticmethod
    def set_run_mode_live():
        redis_helper.set(cons.RUN_MODE, cons.RUN_MODE_LIVE)


if __name__ == "__main__":
    redis_helper.set_run_mode_live()
    print(redis_helper.get_run_mode())

    redis_helper.set_run_mode_testing()
    print(redis_helper.get_run_mode())
