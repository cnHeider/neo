#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from warnings import warn

from neodroid.models import Reaction
from neodroid.neodroid_environments import NeodroidEnvironment
from neodroid.utilities.exceptions.exceptions import NoEnvironmentError

__author__ = 'cnheider'



class SingleEnvironmentWrapper(NeodroidEnvironment):

  def __next__(self):
    if not self._is_connected_to_server:
      return
    return self.react()

  def _react(self,
             input_reaction=None,
             *,
             parameters=None,
             normalise=False,
             **kwargs):
    if not isinstance(input_reaction, Reaction):
      input_reaction = self.maybe_infer_motion_reaction(input_reactions=input_reaction,
                                                        normalise=normalise,
                                                        description=self._description,
                                                        verbose=self._verbose
                                                        )
    if parameters is not None:
      input_reaction.parameters = parameters

    input_reactions = [input_reaction]

    env_states = super()._react(input_reactions=input_reactions, **kwargs)

    first_environment = list(env_states.values())[0]
    if first_environment:
      return first_environment
    raise NoEnvironmentError()

  def _reset(self, input_reaction=None, state=None, on_reset_callback=None):

    input_reaction = self.maybe_infer_configuration_reaction(
        input_reaction=input_reaction,
        description=self._description,
        verbose=self._verbose
        )
    if state:
      input_reaction.unobservables = state.unobservables

    input_reactions = [input_reaction]
    new_states = super()._reset(input_reactions)

    new_state = list(new_states.values())[0]
    return new_state

  def _configure(self, *args, **kwargs):
    message = self._reset(*args, **kwargs)
    if message:
      return message
    return None

  def _describe(self, *args, **kwargs):
    new_states = super()._describe(*args, **kwargs)
    message = list(new_states.values())[0]
    if message:
      return message

    return None

  def _sensor(self, name, *args, **kwargs):
    state_env_0 = list(self._last_message.values())[0]
    observer = state_env_0.sensor(name)
    if not observer:
      warn('Sensor was not found!')
    return observer


if __name__ == '__main__':
  import argparse
  from tqdm import tqdm

  parser = argparse.ArgumentParser(description='Single environment wrapper')
  parser.add_argument(
      '--ENVIRONMENT_NAME',
      type=str,
      default='grd',
      metavar='ENVIRONMENT_NAME',
      help='name of the environment to run',
      )
  parser.add_argument(
      '--CONNECT_TO_RUNNING',
      '-C',
      action='store_true',
      default=True,
      help='Connect to already running environment instead of starting another instance')
  proc_args = parser.parse_args()

  env = SingleEnvironmentWrapper(environment_name=proc_args.ENVIRONMENT_NAME,
                                 connect_to_running=proc_args.CONNECT_TO_RUNNING)

  observation_session = tqdm(env, leave=False)
  for environment_state in observation_session:
    if environment_state.terminated:
      print(f'Interrupted {environment_state.signal}')
      env.reset()
