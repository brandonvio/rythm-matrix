import os
from dotenv import load_dotenv


class env:
    load_dotenv()

    @staticmethod
    def get(name):
        return os.getenv(name)
