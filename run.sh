#!/bin/bash

source ~/miniconda3/bin/activate flask
exec gunicorn -b 0.0.0.0.:5000 wsgi:app