#!/bin/bash

echo "[.] Installing python requirements with pip"
pip install -r requirements.txt

python3 daemon.py
