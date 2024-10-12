import json
import logging
from functools import wraps

import redis
from redis_lru import RedisLRU

from models import Author, Quote


logging.basicConfig(level=logging.INFO)

redis_client = redis.Redis(host='localhost', port=6379, db=0)

cache = RedisLRU(redis_client)


def cache(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        key = f"{func.__name__}:{args}:{kwargs}"
        cached_result = redis_client.get(key)
        if cached_result:
            logging.info(f"Fetched data for '{key}' from cache.")
            return json.loads(cached_result.decode('utf-8'))  
        result = func(*args, **kwargs)
        redis_client.set(key, json.dumps(result))
        logging.info(f"Fetched data for '{key}' from the database.")
        return result
    return wrapper


@cache
def get_quotes_by_author(author_name):
    author = Author.objects(fullname__istartswith=author_name).first()
    if author:
        quotes = Quote.objects(author=author)
        logging.info(f"Fetched {len(quotes)} quotes for author '{author_name}' from the database.")
        return [q.quote for q in quotes]
    logging.info(f"No quotes found for author '{author_name}'.")
    return []

@cache
def get_quotes_by_tag(tag):
    quotes = Quote.objects(tags__icontains=tag)
    logging.info(f"Fetched {len(quotes)} quotes for tag '{tag}' from the database.")
    return [q.quote for q in quotes]

@cache
def get_quotes_by_tags(tags):
    quotes = []
    for tag in tags:
        quotes += get_quotes_by_tag(tag.strip())
        if quotes:
            logging.info(f"Fetched {len(quotes)} quotes for tag '{tag.strip()}' from the database.")
        else:
            logging.info(f"No quotes found for tag '{tag.strip()}'.")
    return list(set(quotes))