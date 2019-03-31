#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'cnheider'

import time
from abc import ABC

from tqdm import tqdm

import neodroid.models as M
from neodroid import messaging
from neodroid.environment import Environment
from neodroid.neodroid_utilities import (ClientEvents,
                                         construct_action_space,
                                         construct_observation_space,
                                         message_client_event,
                                         )

CONNECT_TRY_TIMES = 100
CONNECT_TRY_INTERVAL = 0.1


class NetworkingEnvironment(Environment, ABC):

  def __init__(self,
               *,
               ip='localhost',
               port=6969,
               connect_to_running=False,
               on_connected_callback=None,
               on_disconnected_callback=None,
               on_timeout_callback=None,
               **kwargs):
    super().__init__(**kwargs)

    # Networking
    self._ip = ip
    self._port = port
    self._connect_to_running = connect_to_running
    self._external_on_connected_callback = on_connected_callback
    self._external_on_disconnected_callback = on_disconnected_callback
    self._external_on_timeout_callback = on_timeout_callback

  def __next__(self):
    if not self._is_connected_to_server:
      return
    return self._react()

  def _setup_connection(self):
    print(f'Connecting to server at {self._ip}:{self._port}')

    connect_tries = tqdm(range(CONNECT_TRY_TIMES), leave=False)

    self._message_server = messaging.MessageClient(self._ip,
                                                   self._port,
                                                   on_timeout_callback=self.__on_timeout_callback__,
                                                   on_connected_callback=self.__on_connected_callback__,
                                                   on_disconnected_callback=self.__on_disconnected_callback__,
                                                   verbose=self._verbose,writer=connect_tries.write)


    self._describe()

    while self.description is None:
      self._describe()
      time.sleep(CONNECT_TRY_INTERVAL)
      connect_tries.update()
      connect_tries.set_description(f'Connecting, please make sure that the ip {self._ip} '
                                    f'and port {self._port} '
                                    f'are cd correct')
      if connect_tries.n is CONNECT_TRY_TIMES:
        raise ConnectionError

    # TODO: WARN ABOUT WHEN INDIVIDUAL OBSERVATIONS AND UNOBSERVABLES ARE UNAVAILABLE
    # due to simulator configuration

    self._is_connected_to_server = True

  @message_client_event(event=ClientEvents.CONNECTED)
  def __on_connected_callback__(self):
    '''

'''
    if self._external_on_connected_callback:
      self._external_on_connected_callback()

  @message_client_event(event=ClientEvents.DISCONNECTED)
  def __on_disconnected_callback__(self):
    '''

'''
    self._is_connected_to_server = False
    if self._external_on_disconnected_callback:
      self._external_on_disconnected_callback()

  @message_client_event(event=ClientEvents.TIMEOUT)
  def __on_timeout_callback__(self):
    '''

'''
    if self._external_on_timeout_callback:
      self._external_on_timeout_callback()

  @property
  def is_connected(self):
    return self._is_connected_to_server

  def describe(self):
    return self._describe(parameters=M.ReactionParameters(
        terminable=False, describe=True, episode_count=False
        ))

  def _describe(
      self,
      parameters=M.ReactionParameters(terminable=True,
                                      describe=True,
                                      episode_count=False)
      ):
    '''

:param parameters:
:type parameters:
:return:
:rtype:
'''
    new_states, simulator_configuration = self._message_server.send_reactions(
        [M.Reaction(parameters=parameters)])
    if new_states:

      self.update_interface_statics(new_states, simulator_configuration)
      return new_states

  def update_interface_statics(self, new_states, new_simulator_configuration):
    self._last_message = new_states
    # flat_message = flattened_observation(new_state)
    self._simulator_configuration = new_simulator_configuration
    first_environment = list(self._last_message.values())[0]
    self._observation_space = construct_observation_space(first_environment)
    if first_environment.description:
      self._description = first_environment.description
      self._action_space = construct_action_space(self._description)

  def __str__(self):
    return (f'<NetworkingEnvironment>\n'
            f'  <ObservationSpace>{self.observation_space}</ObservationSpace>\n'
            f'  <ActionSpace>{self.action_space}</ActionSpace>\n'
            f'  <Description>{self.description}</Description>\n'
            f'  <IsConnected>{self.is_connected}</IsConnected>\n'
            f'</NetworkingEnvironment>')
