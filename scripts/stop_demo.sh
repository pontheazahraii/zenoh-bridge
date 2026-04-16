#!/usr/bin/env bash
pkill -f zenoh-bridge-ros2dds || true
pkill -f demo_nodes_cpp || true
pkill -f "python python/action_server.py" || true
pkill -f "python python/action_client.py" || true
pkill -f "python python/service_server.py" || true
pkill -f "python python/service_client.py" || true
pkill -f "python python/topic_publisher.py" || true
pkill -f "python python/topic_subscriber.py" || true
pkill -f "python ros/action_server.py" || true
pkill -f "python ros/action_client.py" || true
pkill -f "python ros/service_server.py" || true
pkill -f "python ros/service_client.py" || true
