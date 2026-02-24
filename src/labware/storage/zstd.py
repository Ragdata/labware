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
import zstandard as zstd


#-------------------------------------------------------------------
# ZstdCompressor Class
#-------------------------------------------------------------------
class ZstdCompressor:
    """ ZSTD Compressor """
    def __init__(self, level=9, zstd_dict=None):
        self.level = level
        if not ((zstd_dict is None) or isinstance(zstd_dict, zstd.ZstdCompressionDict)):
            zstd_dict = zstd.ZstdCompressionDict(zstd_dict)
        compression_params = zstd.ZstdCompressionParameters(write_checksum=False, write_dict_id=False)
        self._compressor = zstd.ZstdCompressor(level=level, compression_params=compression_params, dict_data=zstd_dict)
        self._decompressor = zstd.ZstdDecompressor(dict_data=zstd_dict)

    def compress(self, data: bytes):
        """ Compress bytes data & return compressed bytes """
        return self._compressor.compress(data)

    def decompress(self, data: bytes):
        """ Decompress bytes data & return original bytes """
        return self._decompressor.decompress(data)

    @staticmethod
    def optimize_dict(samples: list[bytes]):
        total_size = sum(map(len, samples))
        dict_size = max(total_size // 100, 256)
        dict_size = min(dict_size, 109_000)
        zstd_dict = zstd.train_dictionary(dict_size, samples)
        return zstd_dict.as_bytes()
