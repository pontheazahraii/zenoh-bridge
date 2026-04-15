#!/usr/bin/env bash
source /opt/ros/humble/setup.bash
export ROS_DISTRO=humble
export ROS_DOMAIN_ID="${ROS_DOMAIN_ID:-42}"
RUST_LOG=info zenoh-bridge-ros2dds
