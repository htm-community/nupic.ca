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
import imp
import math
from collections import deque

import automatatron
from colorama import Fore
from colorama import init as colorama_init
from nupic.frameworks.opf.modelfactory import ModelFactory

MODEL_NAME = "swarm_input"
DATA_DIR = "."
MODEL_PARAMS_DIR = "./model_params"
PREDICTED_FIELD = "bit_10"

def createModel(modelParams):
  model = ModelFactory.create(modelParams)
  model.enableInference({"predictedField": PREDICTED_FIELD})
  return model


def default_string_formatter(row, width=0):
  side_padding = int(math.floor((width - len(row) )/ 2)) * " "
  out = side_padding
  for v in row:
    if v:
      cell = "#"
    else:
      cell  = " "
    out += cell
  out += side_padding
  return out


def getModelParamsForRule(rule_number):
  this_dir = os.path.dirname(os.path.realpath(__file__))
  model_params_path = os.path.join(this_dir, "model_params/rule_%s_model_params.py" % rule_number)
  print "Importing model params from %s" % model_params_path
  importedModelParams = imp.load_source("model_params", model_params_path).MODEL_PARAMS
  return importedModelParams


def print_current_row_with_last_prediction(row, prediction, predicted_index, history):
  string_row = ["#" if i else " " for i in row]
  value = str(row[predicted_index])
  correct = (value == prediction)
  character = string_row[predicted_index]
  color = Fore.RED
  if correct:
    color = Fore.GREEN
  if character == " ":
    character = "."
  string_row[predicted_index] = color + character + Fore.RESET
  if correct: history.append(1.0)
  else: history.append(0.0)
  correctness = reduce(lambda x, y: x + y, history) / len(history)
  print "".join(string_row) + "   " + "{0:.0f}%".format(correctness * 100)
    

def run_io_through_nupic(model, rule_number):
  prediction_history = deque(maxlen=500)
  counter = [0]
  last_prediction = [None]

  def stream_handler(row, _):
    counter[0] += 1
    input_row = {}
    for index, field in enumerate(row):
      input_row["bit_%i" % index] = str(field)
    
    # Show this input row compared with the last prediction
    print_current_row_with_last_prediction(
      row, last_prediction[0], int(PREDICTED_FIELD.split("_").pop()), prediction_history
    )
    result = model.run(input_row)

    prediction = result.inferences["multiStepBestPredictions"][1]
    last_prediction[0] = prediction
    

  automaton = automatatron.Engine(rule_number)
  automaton.run(iterations=21)
  automaton.run(handler=stream_handler, width=21)
  


def run_model(rule_number):
  colorama_init()
  
  print "Creating model for Rule #%s..." % rule_number
  model = createModel(getModelParamsForRule(rule_number))
  run_io_through_nupic(model, int(rule_number))

