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
./scripts/service/ros/server.sh
```

**Terminal 2: Call the service from ROS 2**

```shell
./scripts/service/ros/client.sh 4 7
```

If you omit the arguments, the client uses `2 3`.

#### Expected Result

The server should log the handled request, and the client should print the returned sum.

---

#### Zenoh Only

**Terminal 1: Start Zenoh service server**

```shell
./scripts/service/zenoh/server.sh
```

**Terminal 2: Call the service from Zenoh**

```shell
./scripts/service/zenoh/client.sh 4 7
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
./scripts/service/ros/server.sh
```

**Terminal 2: Start bridge**

```shell
./scripts/start_bridge.sh
```

**Terminal 3: Call the service from Zenoh**

```shell
./scripts/service/zenoh/client.sh
```

#### Expected Result

- the ROS server logs the handled request
- the Zenoh client prints `Response: 2 + 3 = 5`

#### Zenoh Server -> ROS Client

**Terminal 1: Start Zenoh service server**

```shell
./scripts/service/zenoh/server.sh
```

**Terminal 2: Start bridge**

```shell
./scripts/start_bridge.sh
```

**Terminal 3: Call the service from ROS 2**

```shell
./scripts/service/ros/client.sh
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

---

### Action Demo

This repo includes a minimal `Fibonacci` action demo implemented in both ROS 2 and Zenoh.

Action interop with `zenoh-bridge-ros2dds` expects CycloneDDS-compatible ROS middleware behavior.
The ROS action scripts in this repo set:

```shell
RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
ROS_DOMAIN_ID=42
```

#### ROS 2 Only

**Terminal 1: Start ROS 2 action server**

```shell
./scripts/action/ros/server.sh
```

**Terminal 2: Call the action from ROS 2**

```shell
./scripts/action/ros/client.sh 5
```

If you omit the argument, the client uses `5`.

#### Expected Result

The ROS client should log one feedback update followed by the final Fibonacci sequence.

---

#### Zenoh Only

**Terminal 1: Start Zenoh action server**

```shell
./scripts/action/zenoh/server.sh
```

**Terminal 2: Call the action from Zenoh**

```shell
./scripts/action/zenoh/client.sh 5
```

If you omit the argument, the client uses `5`.

#### Expected Result

The Zenoh client should print goal acceptance, one feedback update, and the final Fibonacci sequence.

---

#### Mixed ROS / Zenoh

This repo supports both mixed action directions through `zenoh-bridge-ros2dds`.

#### ROS Server -> Zenoh Client

**Terminal 1: Start ROS 2 action server**

```shell
./scripts/action/ros/server.sh
```

**Terminal 2: Start bridge**

```shell
./scripts/start_bridge.sh
```

**Terminal 3: Call the action from Zenoh**

```shell
./scripts/action/zenoh/client.sh 5
```

#### Expected Result

- the ROS server logs the handled goal
- the Zenoh client prints goal acceptance
- the Zenoh client prints one feedback sequence
- the Zenoh client prints the final result sequence

#### Zenoh Server -> ROS Client

**Terminal 1: Start Zenoh action server**

```shell
./scripts/action/zenoh/server.sh
```

**Terminal 2: Start bridge**

```shell
./scripts/start_bridge.sh
```

**Terminal 3: Call the action from ROS 2**

```shell
./scripts/action/ros/client.sh 5
```

#### Expected Result

- the Zenoh server logs the accepted goal
- the ROS client logs one feedback update
- the ROS client logs the final result sequence

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
./scripts/topic/ros/talker.sh
```

**Terminal 2: Start bridge**

```shell
./scripts/start_bridge.sh
```

**Terminal 3: Run Python subscriber**

```shell
./scripts/topic/zenoh/subscriber.sh
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
./scripts/topic/ros/listener.sh
```

**Terminal 2: Start bridge**

```shell
./scripts/start_bridge.sh
```

**Terminal 3: Run Python publisher**

```shell
./scripts/topic/zenoh/publisher.sh
```

#### Expected Result

The ROS 2 listener should receive repeated samples from the bridged ROS 2 `/chatter` topic, confirming:

- Zenoh Python is publishing
- bridge is active
- ROS 2 subscriber is connected
- Zenoh topic data is reaching ROS 2

## Cleanup

Before rerunning a mixed demo, stop any old bridge or demo processes:

```shell
./scripts/stop_demo.sh
```

If you start multiple bridge or demo instances without stopping the old ones, requests, feedback, and results may appear multiple times.
