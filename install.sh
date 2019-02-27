#!/usr/bin/env bash

virtualenv env
source env/bin/activate
pip install -r requirements.txt requirements/dev.txt
pip install --editable .
