#!/usr/bin/env python3
"""
====================================================================
Package: labware
====================================================================
Author:			Ragdata
Date:			22/02/2026
License:		MIT License
Repository:		https://github.com/Ragdata/labware
Copyright:		Copyright © 2026 Redeyed Technologies
====================================================================
"""
import sqlite3, time, hashlib, pickle, random

from pathlib import Path
from functools import wraps
from typing import Callable, Any, Optional
from cachetools import TTLCache, LRUCache

from . sqlite import _Database
from . serializer import PickleSerializer


#-------------------------------------------------------------------
# Exception Class
#-------------------------------------------------------------------
class SqlCacheError(Exception):
    pass


#-------------------------------------------------------------------
# _SqlCacheDatabase Class
#-------------------------------------------------------------------
class _SqlCacheDatabase:
    """ SQLite cache database """

    BUILD_TABLE = """
        CREATE TABLE IF NOT EXISTS cache (
            key TEXT UNIQUE NOT NULL PRIMARY KEY,
            value BLOB NOT NULL,
            created_at REAL NOT NULL,
            access_count INTEGER DEFAULT 0,
            last_access REAL NOT NULL
        )
    """

    CREATE_INDEX = """
        CREATE INDEX IF NOT EXISTS idx_created_at ON cache(created_at)
    """

    CREATE_ACCESS_INDEX = """
        CREATE INDEX IF NOT EXISTS idx_last_access ON cache(last_access)
    """

    def __init__(self, cache_path: str, multiprocess_safe: bool = True):
        self.cache_path = Path(cache_path)
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        self.multiprocess_safe = multiprocess_safe
        sqlite3_kargs = {}
        if multiprocess_safe:
            sqlite3_kargs = { "check_same_thread": False }
        self._db = _Database(str(self.cache_path), flag="c", mode=0o666, sqlite3_kargs=sqlite3_kargs)
        if multiprocess_safe:
            self._optimize_for_multiprocess()
        self._execute(self.BUILD_TABLE)
        self._execute(self.CREATE_INDEX)
        self._execute(self.CREATE_ACCESS_INDEX)
        self.serializer = PickleSerializer()

    def _execute(self, sql: str, params: tuple = ()):
        if not self.multiprocess_safe:
            try:
                return self._db.execute(sql, params)
            except Exception as e:
                raise SqlCacheError(f"Database Operation Failed: {e}")
        max_retries = 5
        base_delay = 0.1
        for attempt in range(max_retries):
            try:
                return self._db.execute(sql, params)
            except sqlite3.OperationalError as exc:
                if "database is locked" in str(exc).lower() and attempt < max_retries - 1:
                    delay = base_delay * (2 ** attempt) + random.uniform(0, 0.1)
                    time.sleep(delay)
                    continue
                else:
                    raise SqlCacheError(f"Database is locked, likely due to multiple simultaneous operations.  Try again later: {exc}")
            except Exception as e:
                raise SqlCacheError(f"Database Operation Failed: {e}")
        return None

    @staticmethod
    def _generate_key(func_name: str, args: tuple, kwargs: dict) -> str:
        key_data = (func_name, args, tuple(sorted(kwargs.items())))
        key_bytes = pickle.dumps(key_data)
        return hashlib.md5(key_bytes).hexdigest()

    def _optimize_for_multiprocess(self):
        """ Optimize SQLite settings for multiprocess environments """
        try:
            # PRAGMA settings optimized for multiprocess environments
            self._db._cx.execute("PRAGMA journal_mode = wal")
            self._db._cx.execute("PRAGMA synchronous = normal")
            self._db._cx.execute("PRAGMA busy_timeout = 30000")
            self._db._cx.execute("PRAGMA cache_size = -20000")
            self._db._cx.execute("PRAGMA temp_store = MEMORY")
            self._db._cx.execute("PRAGMA mmap_size = 268435456")
            self._db._cx.execute("PRAGMA page_size = 4096")
        except sqlite3.OperationalError:
            pass

    def cleanup_expired(self, ttl: float):
        current_time = time.time()
        self._execute("DELETE FROM cache WHERE created_at < ?", (current_time - ttl,))

    def cleanup_lru(self, max_size: int):
        with self._execute("SELECT COUNT(*) FROM cache") as cursor:
            count = cursor.fetchone()[0]
        if count > max_size:
            excess = count - max_size
            self._execute("DELETE FROM cache WHERE key IN (SELECT key FROM cache ORDER BY last_access ASC LIMIT ?)", (excess,))

    def clear(self):
        self._execute("DELETE FROM cache")

    def close(self):
        if hasattr(self, "_db"):
            self._db.close()

    def delete(self, key: str):
        self._execute("DELETE FROM cache WHERE key = ?", (key,))

    def get(self, key: str, ttl: Optional[float] = None) -> Optional[Any]:
        current_time = time.time()
        if ttl:
            query = "SELECT value, created_at FROM cache WHERE key = ? AND created_at > ?"
            params = (key, current_time - ttl)
        else:
            query = "SELECT value, created_at FROM cache WHERE key = ?"
            params = (key,)
        with self._execute(query, params) as cursor:
            row = cursor.fetchone()
            if row:
                self._execute("UPDATE cache SET access_count = access_count + 1, last_access = ? WHERE key = ?", (current_time, key))
                compressed_value = row[0]
                decompressed_value = self._db.compressor.decompress(compressed_value)
                return self.serializer.unserialize(decompressed_value)
        return None

    def get_stats(self) -> dict:
        with self._execute("SELECT COUNT(*), AVG(access_count), MAX(last_access) FROM cache") as cursor:
            row = cursor.fetchone()
            return {"total_items": row[0] or 0, "avg_access_count": row[1] or 0, "last_access": row[2] or 0}

    def set(self, key: str, value: Any):
        current_time = time.time()
        serialized_value = self.serializer.serialize(value)
        compressed_value = self._db.compressor.compress(serialized_value)
        self._execute("INSERT OR REPLACE INTO cache (key, value, created_at, access_count, last_access) VALUES (?, ?, ?, ?, ?)", (key, compressed_value, current_time, 1, current_time),)


#-------------------------------------------------------------------
# SqlCache Class
#-------------------------------------------------------------------
class SqlCache:
    """ Sqlite cache """

    def __init__(self, cache_path: str = "cache.db", max_size: int = 1000, ttl: Optional[float] = None, cache_type: str = "lru", multiprocess_safe: bool = True):
        self.cache_path = cache_path
        self.max_size = max_size
        self.ttl = ttl
        self.cache_type = cache_type.lower()
        self.multiprocess_safe = multiprocess_safe
        if self.cache_type not in ["ttl", "lru"]:
            raise ValueError("cache_type must be 'ttl' or 'lru'")
        self._db = _SqlCacheDatabase(cache_path, multiprocess_safe=multiprocess_safe)
        if self.cache_type == "ttl":
            self._memory_cache = TTLCache(maxsize=max_size, ttl=ttl or 3600)
        else:
            self._memory_cache = LRUCache(maxsize=max_size)

    def __call__(self, func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = self._db._generate_key(func.__name__, args, kwargs)
            if cache_key in self._memory_cache:
                return self._memory_cache[cache_key]
            cached_value = self._db.get(cache_key, self.ttl)
            if cached_value is not None:
                self._memory_cache[cache_key] = cached_value
                return cached_value
            result = func(*args, **kwargs)
            self._db.set(cache_key, result)
            self._memory_cache[cache_key] = result
            self._cleanup()
            return result
        return wrapper

    def _cleanup(self):
        if self.cache_type == "ttl" and self.ttl:
            self._db.cleanup_expired(self.ttl)
        else:
            self._db.cleanup_lru(self.max_size)

    def clear(self):
        self._db.clear()
        self._memory_cache.clear()

    def close(self):
        self._db.close()

    def get_stats(self) -> dict:
        db_stats = self._db.get_stats()
        return {"disk_cache": db_stats, "memory_cache_size": len(self._memory_cache), "cache_type": self.cache_type, "max_size": self.max_size, "ttl": self.ttl}


#-------------------------------------------------------------------
# MODULE FUNCTIONS
#-------------------------------------------------------------------
def sqlcache(cache_path: str = "cache.db", max_size: int = 1000, ttl: Optional[float] = None, cache_type: str = "lru", multiprocess_safe: bool = True):
    cache = SqlCache(cache_path=cache_path, max_size=max_size, ttl=ttl, cache_type=cache_type, multiprocess_safe=multiprocess_safe)
    return cache

def ttl_cache(cache_path: str = "cache.db", max_size: int = 1000, ttl: float = 3600, multiprocess_safe: bool = True):
    return sqlcache(cache_path=cache_path, max_size=max_size, ttl=ttl, cache_type="ttl", multiprocess_safe=multiprocess_safe)

def lru_cache(cache_path: str = "cache.db", max_size: int = 1000, multiprocess_safe: bool = True):
    return sqlcache(cache_path=cache_path, max_size=max_size, cache_type="lru", multiprocess_safe=multiprocess_safe)
