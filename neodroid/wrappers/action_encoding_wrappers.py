#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
from typing import Any

from neodroid.neodroid_utilities.encodings import signed_ternary_encoding
from neodroid.wrappers.gym_wrapper import NeodroidGymWrapper

__author__ = 'cnheider'

from neodroid.wrappers.curriculum_wrapper import NeodroidCurriculumWrapper


class BinaryActionEncodingWrapper(NeodroidGymWrapper):

  def step(self, action: int = 0, **kwargs) -> Any:
    ternary_action = signed_ternary_encoding(self.action_space.num_motors, action)
    return super().step(ternary_action, **kwargs)

  @property
  def action_space(self):
    self.act_spc = super().action_space

    # self.act_spc.sample = self.signed_one_hot_sample

    return self.act_spc

  def signed_one_hot_sample(self):
    num = self.act_spc.num_binary_actions
    return random.randrange(num)


class BinaryActionEncodingCurriculumEnvironment(NeodroidCurriculumWrapper):

  def step(self, action: int = 0, **kwargs) -> Any:
    a = signed_ternary_encoding(self.action_space.num_motors, action)
    return super().act(input_reaction=a, **kwargs)

  @property
  def action_space(self):
    self.act_spc = super().action_space

    # self.act_spc.sample = self.signed_one_hot_sample

    return self.act_spc

  def signed_one_hot_sample(self):
    num = self.act_spc.num_binary_actions
    return random.randrange(num)
