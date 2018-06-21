#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from neodroid.wrappers.single_environment_wrapper import SingleEnvironmentWrapper

__author__ = 'cnheider'

from neodroid.utilities import flattened_observation


class FlaskWrapper(SingleEnvironmentWrapper):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

  def __next__(self):
    if not self._is_connected_to_server:
      return
    return self.act()

  def act(self, *args, **kwargs):
    message = super().react(*args, **kwargs)
    first_environment = list(message.values())[0]  # TODO: Only exposing first environments state
    if first_environment:
      return (
        flattened_observation(first_environment),
        first_environment.signal,
        first_environment.terminated,
        first_environment
        )
    return None, None, None, None

  def realise(self):
    pass

  def configure(self, *args, **kwargs):
    message = super().reset(*args, **kwargs)
    if message:
      return flattened_observation(message), message
    return None, None

  def observe(self, *args, **kwargs):
    message = super().observe(*args, **kwargs)
    if message:
      return (
        flattened_observation(message),
        message.signal,
        message.terminated,
        message,
        )
    return None, None, None, None

  def quit(self, *args, **kwargs):
    return self.close(*args, **kwargs)
