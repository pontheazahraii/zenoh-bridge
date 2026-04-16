#!/usr/bin/env bash
pkill -f zenoh-bridge-ros2dds || true
pkill -f demo_nodes_cpp || true
pkill -f "python python/action/server.py" || true
pkill -f "python python/action/client.py" || true
pkill -f "python python/service/server.py" || true
pkill -f "python python/service/client.py" || true
pkill -f "python python/topic/publisher.py" || true
pkill -f "python python/topic/subscriber.py" || true
pkill -f "python ros/action/server.py" || true
pkill -f "python ros/action/client.py" || true
pkill -f "python ros/service/server.py" || true
pkill -f "python ros/service/client.py" || true
