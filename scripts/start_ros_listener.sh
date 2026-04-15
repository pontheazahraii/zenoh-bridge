#!/usr/bin/env bash
source /opt/ros/humble/setup.bash
export ROS_DOMAIN_ID="${ROS_DOMAIN_ID:-42}"
ros2 run demo_nodes_cpp listener
