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
import sys
import os
import re
from optparse import OptionParser

from nupicca import (requires_swarm_input, requires_swarm, 
                     create_swarm_input, run_swarm, run_model)

DEFAULT_RULE = 30

parser = OptionParser(
  usage="%prog <path/to/wav> [options]\n\nConvert wav file into NuPIC input."
)

parser.add_option(
  "-r",
  "--rule_number",
  dest="rule_number",
  default=DEFAULT_RULE,
  help="Which elementary cellular automata rule to run.")
parser.add_option(
  "-c",
  "--clean",
  action="store_true",
  dest="clean",
  default=False,
  help="Cleans up temporary files and exits."
)


def clean_temp_files():
  this_dir = os.path.dirname(os.path.realpath(__file__))
  def purge(directory, pattern):
    for f in os.listdir(directory):
      if re.search(pattern, f):
        os.remove(os.path.join(directory, f))
  purge(os.path.join(this_dir, "nupicca/data"), "\.py$")
  purge(os.path.join(this_dir, "nupicca/data"), "\.csv$")
  purge(os.path.join(this_dir, "nupicca/model_params"), "^rule_")

if __name__ == "__main__":
  (options, args) = parser.parse_args(sys.argv[1:])
  rule_number = options.rule_number

  if options.clean:
    clean_temp_files()
    exit()
  
  if requires_swarm_input(rule_number):
    print "No input data found for Rule #%s!" % rule_number
    print "Creating swarm input for Rule #%s..." % rule_number
    create_swarm_input(rule_number)

  if requires_swarm(rule_number):
    print "No model params found for Rule #%s!" % rule_number
    print "Running swarm for Rule #%s..." % rule_number
    run_swarm(rule_number)
  
  run_model(rule_number)