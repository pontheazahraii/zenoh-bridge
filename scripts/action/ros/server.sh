#!/usr/bin/env bash
source /opt/ros/humble/setup.bash
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
export ROS_DOMAIN_ID="${ROS_DOMAIN_ID:-42}"
source .venv/bin/activate
python ros/action/server.py
