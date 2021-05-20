#!/bin/bash
. TFGM-web/venv/bin/activate
nohup waitress-serve --port=8557 --call 'tfgm:create_app' &
