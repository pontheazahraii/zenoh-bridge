import sys

import rclpy
from example_interfaces.srv import AddTwoInts
from rclpy.node import Node


class AddTwoIntsClient(Node):
    def __init__(self) -> None:
        super().__init__("add_two_ints_client")
        self.client = self.create_client(AddTwoInts, "add_two_ints")

    def call(self, a: int, b: int) -> int:
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("Waiting for /add_two_ints...")

        request = AddTwoInts.Request()
        request.a = a
        request.b = b

        future = self.client.call_async(request)
        rclpy.spin_until_future_complete(self, future)
        result = future.result()
        if result is None:
            raise RuntimeError("Service call failed")
        return result.sum


def parse_args() -> tuple[int, int]:
    if len(sys.argv) == 3:
        return int(sys.argv[1]), int(sys.argv[2])
    return 2, 3


def main() -> None:
    a, b = parse_args()

    rclpy.init()
    node = AddTwoIntsClient()

    try:
        total = node.call(a, b)
        node.get_logger().info(f"Response: {a} + {b} = {total}")
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == "__main__":
    main()
