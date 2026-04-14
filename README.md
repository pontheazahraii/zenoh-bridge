# Zenoh Demo

## Architecture

```text
ROS 2 talker/service node  <- owns ROS types
          ^
          | DDS
          v
zenoh-bridge-ros2dds
          ^
          | Zenoh
          v
Python Zenoh script
```

## Install `zenoh-bridge-ros2dds` on Ubuntu

This demo expects the standalone `zenoh-bridge-ros2dds` binary to be installed and available on your `PATH`.

### Option 1: Install from the Eclipse Zenoh Debian repository

```shell
sudo mkdir -p /etc/apt/keyrings
curl -L https://download.eclipse.org/zenoh/debian-repo/zenoh-public-key | sudo gpg --dearmor --yes --output /etc/apt/keyrings/zenoh-public-key.gpg
echo "deb [signed-by=/etc/apt/keyrings/zenoh-public-key.gpg] https://download.eclipse.org/zenoh/debian-repo/ /" | sudo tee /etc/apt/sources.list.d/zenoh.list > /dev/null
sudo apt update
sudo apt install zenoh-bridge-ros2dds
```

Verify the install:

```shell
command -v zenoh-bridge-ros2dds
zenoh-bridge-ros2dds --help
```

### Option 2: Download the standalone release manually

If you do not want to add the Debian repository, download the latest standalone release from:

- <https://download.eclipse.org/zenoh/zenoh-plugin-ros2dds/latest/>

Choose the archive for your platform, unzip it, and either run the extracted `zenoh-bridge-ros2dds` binary directly or move it somewhere on your `PATH`.

## Python

### Virtual Environment

```shell
python3.10 -m venv .venv
source .venv/bin/activate
```

### Requirements

```shell
pip install -r requirements.txt
pip install -r requirements-dev.txt  # dev requirements
```

## Demos

### Topic Bridge Demo: Subscriber

Verify end-to-end communication between ROS 2, the Zenoh bridge, and a Zenoh Python client.

This demo subscribes to the bridged ROS 2 `/chatter` topic and prints incoming samples.

#### Architecture

```text
ROS 2 talker
    v
DDS
    v
zenoh-bridge-ros2dds
    v
Zenoh
    v
topic_subscriber.py
```

#### Run the Demo

**Terminal 1: Start ROS 2 talker**

```shell
./scripts/start_ros_talker.sh
```

**Terminal 2: Start bridge**

```shell
./scripts/start_bridge.sh
```

**Terminal 3: Run Python subscriber**

```shell
./scripts/run_topic_subscriber.sh
```

#### Expected Result

The subscriber should receive repeated samples from the bridged ROS 2 `/chatter` topic, confirming:

- ROS 2 is publishing
- bridge is active
- Zenoh Python client is connected
- ROS 2 topic data is reaching Zenoh

---

### Topic Bridge Demo: Publisher

Verify end-to-end communication between ROS 2, the Zenoh bridge, and a Zenoh Python client.

This demo publishes to the bridged ROS 2 `/chatter` topic from Zenoh Python and verifies that ROS 2 receives the messages.

#### Architecture

```text
topic_publisher.py
    v
Zenoh
    v
zenoh-bridge-ros2dds
    v
DDS
    v
ROS 2 listener
```

#### Run the Demo

**Terminal 1: Start ROS 2 listener**

```shell
./scripts/start_ros_listener.sh
```

**Terminal 2: Start bridge**

```shell
./scripts/start_bridge.sh
```

**Terminal 3: Run Python publisher**

```shell
./scripts/run_topic_publisher.sh
```

#### Expected Result

The ROS 2 listener should receive repeated samples from the bridged ROS 2 `/chatter` topic, confirming:

- Zenoh Python is publishing
- bridge is active
- ROS 2 subscriber is connected
- Zenoh topic data is reaching ROS 2
