import os
from random import randint
import time

from dotenv import load_dotenv
import redis


def main():
    load_dotenv()
    conn_pool = redis.ConnectionPool(
        host=os.environ['REDIS_HOST'],
        port=os.environ.get('REDIS_PORT', 6379),
        password=os.environ['REDIS_PASSWORD'],
    )

    retention_time = 30_000  # 30 seconds
    r = redis.Redis(connection_pool=conn_pool, decode_responses=True)
    ts = r.ts()
    if not r.exists("indicator"):
        ts.create("indicator", labels={"name": "indicator"}, retention_msecs=retention_time)

    while True:
        value = randint(1, 10)  # generate random value between 1 and 10 inclusive
        ts.add("indicator", "*", value)
        time.sleep(1)  # insert value every 1 second


if __name__ == '__main__':
    main()
