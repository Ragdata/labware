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
import collections.abc, json

from functools import partial
from typing import Any

from . import serializer
from . import sqlite

__all__ = ["Shelf", "DbfilenameStorage", "open"]


#-------------------------------------------------------------------
# _ClosedDict Class
#-------------------------------------------------------------------
class _ClosedDict(collections.abc.MutableMapping):
    """ Marker for a closed dictionary.  Access raises a ValueError """

    def closed(self, *args):
        raise ValueError("Invalid operation on closed dictionary")

    __iter__ = __len__ = __getitem__ = __setitem__ = __delitem__ = keys = closed

    def __repr__(self):
        return "<Closed Dictionary>"


#-------------------------------------------------------------------
# Shelf Class
#-------------------------------------------------------------------
class Shelf(collections.abc.MutableMapping):
    """ Base class for shelf implementations """

    def __init__(self, dict: sqlite._Database, writeback=False, keyencoding="utf-8", serialer=None):
        self.dict = dict
        self.writeback = writeback
        self.cache = {}
        self.keyencoding = keyencoding
        if serialer is None:
            self.serializer = serializer.PickleSerializer()
        else:
            self.serializer = serializer.BaseSerializer = serialer

    def __contains__(self, key: str) -> bool:
        return key in self.dict

    def __del__(self):
        if not hasattr(self, "writeback"):
            return
        self.close()

    def __delitem__(self, key: str):
        del self.dict[key]
        try:
            del self.cache[key]
        except KeyError:
            pass

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def __getitem__(self, key: str) -> Any:
        try:
            value = self.cache[key]
        except KeyError:
            f = self.dict[key]
            value = self.serializer.unserialize(f)
            if self.writeback:
                self.cache[key] = value
        return value

    def __iter__(self):
        for k in self.dict.keys():
            yield k

    def __len__(self):
        return len(self.dict)

    def __setitem__(self, key: str, value: dict):
        if self.writeback:
            self.cache[key] = value
        self.dict[key] = self.serializer.serialize(value)

    def close(self):
        if self.dict is None:
            return
        try:
            self.sync()
            try:
                self.dict.close()
            except AttributeError:
                pass
        finally:
            try:
                self.dict = _ClosedDict()
            except:
                self.dict = None

    def get(self, key: str, default: Any = None) -> Any:
        if key in self.dict:
            return self[key]
        return default

    def sync(self):
        if self.writeback and self.cache:
            self.writeback = False
            for key, entry in self.cache.items():
                self[key] = entry
            self.writeback = True
            self.cache = {}
        if hasattr(self.dict, "sync"):
            self.dict.sync()


#-------------------------------------------------------------------
# DbfilenameShelf Class
#-------------------------------------------------------------------
class DbfilenameShelf(Shelf):
    """ Shelf implementation using the generic dbm interface """

    def __init__(self, filename, flag="c", writeback=False, serialer=None):
        sqlite3_kargs = dict(autocommit=True, check_same_thread=False)
        Shelf.__init__(self, dict=sqlite.open(filename, flag, sqlite3_kargs=sqlite3_kargs), writeback=writeback, serialer=serialer)

    def clear(self):
        self.cache.clear()
        self.dict.clear()


#-------------------------------------------------------------------
# MODULE FUNCTIONS
#-------------------------------------------------------------------
def open(filename, flag="c", writeback=False, serialer=None):
    return DbfilenameShelf(filename, flag, writeback, serialer=serialer)
