import os

def cfg(key, default=None):
    return os.getenv(key, default)