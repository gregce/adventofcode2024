import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev'
    OPENAI_API_KEY = None

    @classmethod
    def set_openai_key(cls, key):
        cls.OPENAI_API_KEY = key

    @classmethod
    def get_openai_key(cls):
        return cls.OPENAI_API_KEY or os.environ.get('OPENAI_API_KEY')