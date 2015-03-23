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
import csv
import automatatron

BITS = 21
DATA_DIR = "data"
SWARM_DESC_FILENAME = "swarm_description.tmpl"
SWARM_INPUT_FILENAME = "swarm_input_%s.csv"

def create_swarm_input(rule_number):
  this_dir = os.path.dirname(os.path.realpath(__file__))
  data_dir = os.path.join(this_dir, DATA_DIR)
  swarm_input_file = os.path.join(data_dir, SWARM_INPUT_FILENAME % rule_number)
  
  swarm_desc_file = os.path.join(data_dir, SWARM_DESC_FILENAME)
  with open(swarm_desc_file, "r") as swarm_desc_tmpl:
    swarm_desc = swarm_desc_tmpl.read()
    incl_fields = []
    midpoint = BITS / 2
    for i in xrange(BITS):
      incl_fields.append(dict(
        fieldName="bit_%i" % i,
        fieldType="string"
      ))
    swarm_desc = swarm_desc.replace("<INCLUDED_FIELDS>", str(incl_fields))
    swarm_desc = swarm_desc.replace("<PREDICTED_FIELD>", "bit_%i" % midpoint)
    swarm_desc = swarm_desc.replace("<RULE_NUMBER>", str(rule_number))
    swarm_desc = swarm_desc.replace("<SOURCE_FILE>", swarm_input_file)
    swarm_desc_out = os.path.join(data_dir, "swarm_description_%s.py" % rule_number)
    print "Creating swarm description at %s..." % swarm_desc_out
    with open(swarm_desc_out, "w") as swarm_desc_out:
      swarm_desc_out.write(swarm_desc)
  
  print "Creating swarm input file at %s..." % swarm_input_file
  with open(swarm_input_file, "w") as input_file:
    writer = csv.writer(input_file)
    names = []
    types = []
    flags = []
    for i in xrange(BITS):
      names.append("bit_%i" % i)
      types.append("string")
      flags.append("")
    writer.writerow(names)
    writer.writerow(types)
    writer.writerow(flags)
  
    automaton = automatatron.Engine(int(rule_number))
    def stream_handler(row, _):
      writer.writerow(row)
  
    automaton.run(iterations=BITS)
  
    automaton.run(handler=stream_handler, width=BITS, iterations=3000)
