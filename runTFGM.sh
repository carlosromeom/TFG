#!/bin/bash
. tfgm/venv/bin/activate
nohup waitress-serve --port=8557 --call 'tfgm:create_app' &
