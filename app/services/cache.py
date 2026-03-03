from datetime import datetime, timedelta

_cache = {}

CACHE_TTL_MINUTES = 15

def get_cached(question: str) -> dict | None:
  key = question.strip().lower()
  if key not in _cache:
    return None
  entry = _cache[key]
  if datetime.now() > entry["expires_at"]:
    del _cache[key]
    return None
  return entry

def set_cache(question: str, result: str, sql: str):
  key = question.strip().lower()
  _cache[key] = {
    "result": result,
    "sql": sql,
    "expires_at": datetime.now() + timedelta(minutes=CACHE_TTL_MINUTES),
    "cached_at": datetime.now().strftime("%H:%M:%S")
  }

def clear_cache():
  _cache.clear()
