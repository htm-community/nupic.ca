#!/usr/bin/env python
import importlib
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


def getModelParamsFromName(gymName):
  importName = "model_params.%s_model_params" % (
    gymName.replace(" ", "_").replace("-", "_")
  )
  print "Importing model params from %s" % importName
  try:
    importedModelParams = importlib.import_module(importName).MODEL_PARAMS
  except ImportError:
    raise Exception("No model params exist for '%s'. Run swarm first!"
                    % gymName)
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
    

def run_io_through_nupic(model):
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
    

  automaton = automatatron.Engine(30)
  automaton.run(iterations=21)
  automaton.run(handler=stream_handler, width=21)
  


def runModel(model_name):
  print "Creating model from %s..." % model_name
  model = createModel(getModelParamsFromName(model_name))
  run_io_through_nupic(model)



if __name__ == "__main__":
  colorama_init()
  runModel(MODEL_NAME)