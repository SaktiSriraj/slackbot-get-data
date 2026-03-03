import os
import json
from datetime import datetime
from upstash_redis import Redis
from dotenv import load_dotenv

load_dotenv()

redis = Redis(
    url=os.environ["UPSTASH_REDIS_REST_URL"],
    token=os.environ["UPSTASH_REDIS_REST_TOKEN"]
)

CACHE_TTL_SECONDS = 15 * 60

def get_cached(question: str) -> dict | None:
    key = question.strip().lower()
    print(f"CACHE CHECK: '{key}'")
    try:
        data = redis.get(key)
        if data is None:
            print(f"CACHE MISS: '{key}'")
            return None
        print(f"CACHE HIT: '{key}'")
        entry = json.loads(data)
        entry["result"] = entry["result"].encode().decode('unicode_escape')
        return entry
    except Exception as e:
        print(f"CACHE GET ERROR: {str(e)}")
        return None


def set_cache(question: str, result: str, sql: str):
    key = question.strip().lower()
    try:
        entry = {
            "result":    result,
            "sql":       sql,
            "cached_at": datetime.now().strftime("%H:%M:%S")
        }
        redis.set(key, json.dumps(entry), ex=CACHE_TTL_SECONDS)
        print(f"CACHE SET: '{key}'")
    except Exception as e:
        print(f"CACHE SET ERROR: {str(e)}")


def clear_cache():
    try:
        keys = redis.keys("*")
        if keys:
            redis.delete(*keys)
        print("CACHE CLEARED")
    except Exception as e:
        print(f"CACHE CLEAR ERROR: {str(e)}")
