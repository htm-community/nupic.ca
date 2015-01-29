#!/usr/bin/env python
import importlib
import sys
import csv
import math

from colorama import Fore, Back, Style
from colorama import init as colorama_init
from nupic.data.inference_shifter import InferenceShifter
from nupic.frameworks.opf.metrics import MetricSpec
from nupic.frameworks.opf.modelfactory import ModelFactory
from nupic.frameworks.opf.predictionmetricsmanager import MetricsManager

MODEL_NAME = "swarm_input"
DATA_DIR = "."
MODEL_PARAMS_DIR = "./model_params"

_METRIC_SPECS = (
    MetricSpec(field='bit_5', metric='multiStep',
               inferenceElement='multiStepBestPredictions',
               params={'errorMetric': 'aae', 'window': 1000, 'steps': 1}),
    MetricSpec(field='bit_5', metric='trivial',
               inferenceElement='prediction',
               params={'errorMetric': 'aae', 'window': 1000, 'steps': 1}),
    MetricSpec(field='bit_5', metric='multiStep',
               inferenceElement='multiStepBestPredictions',
               params={'errorMetric': 'altMAPE', 'window': 1000, 'steps': 1}),
    MetricSpec(field='bit_5', metric='trivial',
               inferenceElement='prediction',
               params={'errorMetric': 'altMAPE', 'window': 1000, 'steps': 1}),
)


def createModel(modelParams):
  model = ModelFactory.create(modelParams)
  model.enableInference({"predictedField": "bit_5"})
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



def print_current_row_with_last_prediction(row, prediction, predicted_index):
  string_row = ["#" if i == "1" else " " for i in row]
  value = int(row[predicted_index])
  correct = (value == prediction)
  character = string_row[predicted_index]
  color = Fore.RED
  if correct:
    color = Fore.GREEN
  if character == " ":
    character = "."
  string_row[predicted_index] = color + character + Fore.RESET
  print "".join(string_row)
    


def run_io_through_nupic(input_data, model, model_name, plot):
  inputFile = open(input_data, "rb")
  csvReader = csv.reader(inputFile)
  # skip header rows
  csvReader.next()
  csvReader.next()
  csvReader.next()

  shifter = InferenceShifter()

  metricsManager = MetricsManager(_METRIC_SPECS, model.getFieldInfo(),
                                  model.getInferenceType())

  counter = 0
  last_prediction = None
  for row in csvReader:
    counter += 1
    input_row = {}
    for index, field in enumerate(row):
      input_row["bit_%i" % index] = int(field)
    
    # Show this input row compared with the last prediction
    print_current_row_with_last_prediction(
      row, last_prediction, 6
    )
    result = model.run(input_row)
    result.metrics = metricsManager.update(result)

    # if counter % 100 == 0:
    #   print "Read %i lines..." % counter
    #   print ("After %i records, 1-step altMAPE=%f", counter,
    #           result.metrics["multiStepBestPredictions:multiStep:"
    #                          "errorMetric='altMAPE':steps=1:window=1000:"
    #                          "field=bit_5"])
 
    if plot:
      result = shifter.shift(result)

    prediction = int(round(result.inferences["multiStepBestPredictions"][1]))
    last_prediction = prediction

  inputFile.close()



def runModel(model_name, plot=False):
  print "Creating model from %s..." % model_name
  model = createModel(getModelParamsFromName(model_name))
  input_data = "%s/%s.csv" % (DATA_DIR, model_name.replace(" ", "_"))
  run_io_through_nupic(input_data, model, model_name, plot)



if __name__ == "__main__":
  plot = False
  args = sys.argv[1:]
  if "--plot" in args:
    plot = True
  colorama_init()
  runModel(MODEL_NAME, plot=plot)