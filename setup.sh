#!/bin/bash

cd FCCAnalyses
source /cvmfs/fcc.cern.ch/sw/latest/setup.sh 
cd ../

export PYTHONPATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd ):$PYTHONPATH"
export PYTHONPATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/python:$PYTHONPATH"