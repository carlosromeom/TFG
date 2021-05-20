#!/bin/bash
python3 setup.py bdist_wheel

scp dist/tfgm-*-py3-none-any.whl 150.214.111.207:.

# XXX Hay que instalar/actualizar en el servidor este paquete en el virtual environment
# XXX Hay que copiar el config y generar una secret-key, ver Flask doc
