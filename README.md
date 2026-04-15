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

### Service Demo

This repo includes a minimal `AddTwoInts` service demo implemented in both ROS 2 and Zenoh.

Service interop with `zenoh-bridge-ros2dds` expects CycloneDDS-compatible ROS middleware behavior.
The service scripts in this repo set:

```shell
RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
ROS_DOMAIN_ID=42
```

#### ROS 2 Only

**Terminal 1: Start ROS 2 service server**

```shell
./scripts/start_ros_service_server.sh
```

**Terminal 2: Call the service from ROS 2**

```shell
./scripts/run_ros_service_client.sh 4 7
```

If you omit the arguments, the client uses `2 3`.

#### Expected Result

The server should log the handled request, and the client should print the returned sum.

---

#### Zenoh Only

**Terminal 1: Start Zenoh service server**

```shell
./scripts/start_service_server.sh
```

**Terminal 2: Call the service from Zenoh**

```shell
./scripts/run_service_client.sh 4 7
```

If you omit the arguments, the client uses `2 3`.

#### Expected Result

The server should handle the request and the client should print the returned sum.

---

#### Mixed ROS / Zenoh

This repo supports both mixed service directions through `zenoh-bridge-ros2dds`.

#### ROS Server -> Zenoh Client

**Terminal 1: Start ROS 2 service server**

```shell
./scripts/start_ros_service_server.sh
```

**Terminal 2: Start bridge**

```shell
./scripts/start_bridge.sh
```

**Terminal 3: Call the service from Zenoh**

```shell
./scripts/run_service_client.sh
```

#### Expected Result

- the ROS server logs the handled request
- the Zenoh client prints `Response: 2 + 3 = 5`

#### Zenoh Server -> ROS Client

**Terminal 1: Start Zenoh service server**

```shell
./scripts/start_service_server.sh
```

**Terminal 2: Start bridge**

```shell
./scripts/start_bridge.sh
```

**Terminal 3: Call the service from ROS 2**

```shell
./scripts/run_ros_service_client.sh
```

#### Expected Result

- the Zenoh server logs `Handled query: 2 + 3 = 5`
- the ROS client logs the returned sum

This flow depends on all ROS-facing processes using the same middleware and DDS domain.
The scripts in this repo already set the required values, but if you run commands manually, verify:

```shell
echo "$RMW_IMPLEMENTATION"
echo "$ROS_DOMAIN_ID"
echo "$ROS_DISTRO"
```

Expected values for this demo:

```shell
rmw_cyclonedds_cpp
42
humble
```

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
