#!/usr/bin/env python
# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2015, Numenta, Inc.  Unless you have an agreement
# with Numenta, Inc., for a separate license for this software code, the
# following terms and conditions apply:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses.
#
# http://numenta.org/licenses/
# ----------------------------------------------------------------------
import os

from createswarminput import create_swarm_input
from swarm import run_swarm
from modelrunner import run_model

DATA_DIR = "data"
MODEL_PARAMS_DIR = "model_params"
SWARM_INPUT_FILENAME = "swarm_input_%s.csv"
SWARM_DESCRIPTION_FILENAME = "swarm_description_%s.py"
MODEL_PARAMS_FILENAME = "rule_%s_model_params.py"


def file_exists_in_dir(filename, directory):
  this_dir = os.path.dirname(os.path.realpath(__file__))
  data_dir = os.path.join(this_dir, directory)
  expected_file = os.path.join(data_dir, filename)
  print expected_file
  exists = os.path.exists(expected_file)
  print exists
  return exists


def requires_swarm_input(rule_number):
  if not file_exists_in_dir(SWARM_INPUT_FILENAME % rule_number, DATA_DIR):
    return True
  if not file_exists_in_dir(SWARM_DESCRIPTION_FILENAME % rule_number, DATA_DIR):
    return True


def requires_swarm(rule_number):
  return not file_exists_in_dir(MODEL_PARAMS_FILENAME % rule_number, MODEL_PARAMS_DIR)
