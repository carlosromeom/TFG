#!/bin/bash
echo "Do not forget to start venv:"
echo "   . venv/bin/activate"
export FLASK_APP=tfgm
export FLASK_ENV=development
flask run
