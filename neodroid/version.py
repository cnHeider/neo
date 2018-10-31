#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
import os
import time
from warnings import warn

__author__ = 'cnheider'
__version__ = 0.4


def get_version():
  version = os.getenv('VERSION', None)
  if version:
    # Most git tags are prefixed with 'v' (example: v1.2.3) this is
    # never desirable for artifact repositories, so we strip the
    # leading 'v' if it's present.
    return version[1:] if type(version) is str and version.startswith('v') else version
  else:
    # Default version is an ISO8601 compiliant datetime. PyPI doesn't allow
    # the colon ':' character in its versions, and time is required to allow
    # for multiple publications to master in one day. This datetime string
    # uses the 'basic' ISO8601 format for both its date and time components
    # to avoid issues with the colon character (ISO requires that date and
    # time components of a date-time string must be uniformly basic or
    # extended, which is why the date component does not have dashes.
    #
    # Publications using datetime versions should only be made from master
    # to represent the HEAD moving forward.

    now = datetime.datetime.utcnow()
    version = now.strftime('%Y%m%d%H%M%S')
    warn(f'Environment variable VERSION is not set, using datetime: {version}')

    #version = time.time()
    #warn(f'Environment variable VERSION is not set, using timestamp: {version}')

  return version


if __version__ is None:
  __version__ = get_version()

_debug = False


@property
def debug():
  return _debug
