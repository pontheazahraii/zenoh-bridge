#!/usr/bin/env bash
source /opt/ros/humble/setup.bash
source .venv/bin/activate
python ros/service_client.py "$@"
