import redis
from configs import configs

redis_client = redis.from_url(configs.REDIS_LOCK_URL)


def get_lock(key, timeout=300, blocking_timeout=2):
    lock = redis_client.lock(key, timeout=timeout)
    acquired = lock.acquire(blocking=True, blocking_timeout=blocking_timeout)
    if acquired:
        return lock
    else:
        return None


def release_locks(locks):
    for lock in locks:
        lock.release()
