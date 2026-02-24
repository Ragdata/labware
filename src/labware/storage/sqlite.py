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
import os, sqlite3

from pathlib import Path
from contextlib import suppress, closing
from collections.abc import MutableMapping

from . zstd import ZstdCompressor


#-------------------------------------------------------------------
# MODULE DATA
#-------------------------------------------------------------------
BUILD_TABLE = """
CREATE TABLE IF NOT EXISTS Dict (
    key TEXT UNIQUE NOT NULL PRIMARY KEY,
    value BLOB NOT NULL
)
"""
GET_SIZE = "SELECT COUNT (key) FROM Dict"
LOOKUP_KEY = "SELECT value FROM Dict WHERE key = CAST(? AS TEXT)"
STORE_KV = "REPLACE INTO Dict (key, value) VALUES (CAST(? AS TEXT), CAST(? AS BLOB))"
DELETE_KEY = "DELETE FROM Dict WHERE key = CAST(? AS TEXT)"
ITER_KEYS = "SELECT key FROM Dict"
BUILD_ZSTD_TABLE = """
CREATE TABLE IF NOT EXISTS Zstd (
    key TEXT UNIQUE NOT NULL,
    value BLOB NOT NULL
)
"""
LOOKUP_ZSTD = "SELECT value FROM Zstd WHERE key = ?"
STORE_ZSTD = "INSERT OR REPLACE INTO Zstd (key, value) VALUES (?, ?)"

_ERR_CLOSED = "DBM object has already been closed"
_ERR_REINIT = "DBM object does not support reinitialization"


#-------------------------------------------------------------------
# MODULE FUNCTIONS
#-------------------------------------------------------------------
def _normalize_uri(path):
    path = Path(path)
    uri = path.absolute().as_uri()
    while "//" in uri:
        uri = uri.replace("//", "/")
    return uri

def open(filename, /, flag="r", mode=0o666, sqlite3_kargs={}):
    """
    Open a dbm.sqlite3 database and return the dbm object

    The 'filename' parameter is the name of the database file

    The optional 'flag' parameter can be one of:
        'r': (default) open an existing database for read-only access
        'w': open an existing database for read/write access
        'c': create a database if it does not exist; open for read/write access
        'n': always create a new, empty database; open for read/write access

    The optional 'mode' parameter is the Unix file access mode of the database;
    only used when creating a new database; (default: 0o666)
    """
    return _Database(filename, flag=flag, mode=mode, sqlite3_kargs=sqlite3_kargs)


#-------------------------------------------------------------------
# EXCEPTION CLASS
#-------------------------------------------------------------------
class error(OSError):
    pass


#-------------------------------------------------------------------
# _DATABASE CLASS
#-------------------------------------------------------------------
class _Database(MutableMapping):
    """ SQLite Database class """

    def __init__(self, path, /, *, flag, mode, sqlite3_kargs={}):
        if hasattr(self, "cx"):
            raise error(_ERR_REINIT)
        path = os.fsdecode(path)
        match flag:
            case "r":
                flag = "ro"
            case "w":
                flag = "rw"
            case "c":
                flag = "rwc"
                Path(path).touch(mode=mode, exist_ok=True)
            case "n":
                flag = "rwc"
                Path(path).unlink(missing_ok=True)
                Path(path).touch(mode=mode)
            case _:
                raise ValueError(f"Flag must be one of 'r', 'w', 'c', or 'n' - not {flag!r}")
        # We use the URI format when opening the database
        uri = _normalize_uri(path)
        uri = f"{uri}?mode={flag}"
        try:
            self.cx = sqlite3.connect(uri, uri=True, **sqlite3_kargs)
        except sqlite3.Error as exc:
            raise error(str(exc))
        # This is an optimisation only; it's OK if it fails
        with suppress(sqlite3.OperationalError):
            self.cx.execute("PRAGMA journal_mode = wal")
            self.cx.execute("PRAGMA synchronous = normal")
            self.cx.execute("PRAGMA busy_timeout = 5000")
        if flag == "rwc":
            self.execute(BUILD_TABLE)
        self.execute(BUILD_ZSTD_TABLE)
        zstd_dict = self._load_zstd_dict()
        self.compressor = ZstdCompressor(zstd_dict=zstd_dict)

    def __delitem__(self, key):
        with self.execute(DELETE_KEY, (key,)) as cu:
            if not cu.rowcount:
                raise KeyError(key)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def __getitem__(self, key):
        with self.execute(LOOKUP_KEY, (key,)) as cu:
            row = cu.fetchone()
        if not row:
            raise KeyError(key)
        value = self.compressor.decompress(row[0])
        return value

    def __iter__(self):
        try:
            with self.execute(ITER_KEYS) as cu:
                for row in cu:
                    yield row[0]
        except sqlite3.Error as exc:
            raise error(str(exc))

    def __len__(self):
        with self.execute(GET_SIZE) as cu:
            row = cu.fetchone()
        return row[0]

    def __setitem__(self, key, value):
        value = self.compressor.compress(value)
        self.execute(STORE_KV, (key, value))

    def _load_zstd_dict(self):
        with self.execute(LOOKUP_ZSTD, ("dict",)) as cu:
            row = cu.fetchone()
        if row:
            return row[0]
        return None

    def _save_zstd_dict(self, zstd_dict):
        self.execute(STORE_ZSTD, ("dict", zstd_dict))

    def close(self):
        if self.cx:
            self.cx.close()
            self.cx = None

    def execute(self, *args, **kwargs):
        if not self.cx:
            raise error(_ERR_CLOSED)
        try:
            return closing(self.cx.execute(*args, **kwargs))
        except sqlite3.Error as exc:
            raise error(str(exc))

    def keys(self):
        return list(super().keys())

    def optimise_database(self):
        samples = [value for value in self.values()]
        zstd_dict = ZstdCompressor.optimize_dict(samples)
        rows = [(k, v) for k, v in self.items()]
        self.compressor = ZstdCompressor(zstd_dict=zstd_dict)
        [self.__setitem__(k, v) for k, v in rows]
        self._save_zstd_dict(zstd_dict)
        self.execute("VACUUM")
