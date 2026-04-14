import time
import zenoh

# Subscribe to ROS 2 /chatter through the Zenoh bridge
KEY = "chatter"


def on_sample(sample):
    # Prove that Zenoh is receiving bridged ROS 2 traffic.
    payload = bytes(sample.payload.to_bytes())

    print(f"Received sample on {sample.key_expr}")
    print(f"Payload size: {len(payload)} bytes")
    print(f"First 32 bytes: {payload[:32].hex()}")


def main():
    config = zenoh.Config()

    with zenoh.open(config) as session:
        print(f"Subscribed to {KEY}")

        with session.declare_subscriber(KEY, on_sample):
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\nStopping subscriber...")


if __name__ == "__main__":
    main()
