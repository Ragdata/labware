#!/usr/bin/env python3
"""
====================================================================
Package: labware
====================================================================
Author:			Ragdata
Date:			20/02/2026
License:		MIT License
Repository:		https://github.com/Ragdata/labware
Copyright:		Copyright © 2026 Redeyed Technologies
====================================================================
"""
__pkg_name__ = 'labware'
__version__ = '0.1.0'

#-------------------------------------------------------------------
# version
#-------------------------------------------------------------------
def version(output: bool = True):
	"""Print the package version"""
	if output:
		# Print version to console
		print(f"{__pkg_name__.capitalize()} version {__version__}")
	else:
		# Return the version string
		return f"{__version__}"
	return None

