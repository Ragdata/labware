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
import pydantic, pickle, json

from abc import ABCMeta, abstractmethod


#-------------------------------------------------------------------
# BaseSerializer Class
#-------------------------------------------------------------------
class BaseSerializer(metaclass=ABCMeta):
    """ Base Serialization Class """
    @abstractmethod
    def serialize(self, obj):
        raise NotImplementedError('Subclasses must implement this method')

    @abstractmethod
    def unserialize(self, obj: bytes):
        raise NotImplementedError('Subclasses must implement this method')


#-------------------------------------------------------------------
# JsonSerializer Class
#-------------------------------------------------------------------
class JsonSerializer(BaseSerializer):
    """ Serialization Class """
    def serialize(self, obj: dict):
        jsons = json.dumps(obj, indent=None, ensure_ascii=False, separators=(',', ':'))
        return jsons.encode('utf-8')

    def unserialize(self, obj: bytes):
        return json.loads(obj)


#-------------------------------------------------------------------
# PickleSerializer Class
#-------------------------------------------------------------------
class PickleSerializer(BaseSerializer):
    """ Serialization Class """
    def __init__(self, protocol=None):
        if protocol is None:
            protocol = 5
        self.protocol = protocol

    def serialize(self, obj: dict):
        return pickle.dumps(obj, protocol=self.protocol)

    def unserialize(self, obj: bytes):
        return pickle.loads(obj)


#-------------------------------------------------------------------
# PydanticSerializer Class
#-------------------------------------------------------------------
class PydanticSerializer(BaseSerializer):
    """ Serialization Class """
    def __init__(self, model: pydantic.BaseModel):
        self.model = model

    def serialize(self, obj: pydantic.BaseModel):
        return obj.model_dump_json(exclude_unset=True, indent=None).encode('utf-8')

    def unserialize(self, obj: bytes):
        return self.model.model_validate_json(obj)
