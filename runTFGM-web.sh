#!/bin/bash
. TFGM-web/venv/bin/activate
nohup waitress-serve --port=8557 --call 'TFGM-web:create_app' &
