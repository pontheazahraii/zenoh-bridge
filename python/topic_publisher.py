import time
from rclpy.serialization import serialize_message
from std_msgs.msg import String
import zenoh

# Publish to ROS 2 /chatter through the Zenoh bridge
KEY = "chatter"


def main() -> None:
    with zenoh.open(zenoh.Config()) as session:
        count = 0

        try:
            while True:
                message = f"Hello from Zenoh {count}"
                ros_message = String()
                ros_message.data = message
                payload = serialize_message(ros_message)

                session.put(KEY, payload, encoding=zenoh.Encoding.APPLICATION_CDR)

                print(f"Published to {KEY}: {message}")

                count += 1
                time.sleep(1)

        except KeyboardInterrupt:
            print("\nStopping publisher...")


if __name__ == "__main__":
    main()
