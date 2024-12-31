#!/bin/bash

# Set the FLASK_APP environment variable
export FLASK_APP=api/api_server.py

# Set the FLASK_ENV environment variable
export FLASK_ENV=development

# Add project root to PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Run the Flask development server
flask run --host=0.0.0.0
