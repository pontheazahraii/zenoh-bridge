import sys
import time

import rclpy
from example_interfaces.action import Fibonacci
from rclpy.action import ActionClient
from rclpy.node import Node

SERVER_WAIT_TIMEOUT = 15.0


class FibonacciActionClient(Node):
    def __init__(self) -> None:
        super().__init__("fibonacci_action_client")
        self._action_client = ActionClient(self, Fibonacci, "fibonacci")

    def feedback_callback(self, feedback_msg) -> None:
        feedback = list(feedback_msg.feedback.sequence)
        self.get_logger().info(f"Feedback: {feedback}")

    def send_goal(self, order: int) -> tuple[int, list[int]]:
        deadline = time.time() + SERVER_WAIT_TIMEOUT
        while not self._action_client.wait_for_server(timeout_sec=1.0):
            self.get_logger().info("Waiting for /fibonacci...")
            if time.time() >= deadline:
                raise RuntimeError("Timed out waiting for /fibonacci action server")

        goal_msg = Fibonacci.Goal()
        goal_msg.order = order

        goal_future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback,
        )
        rclpy.spin_until_future_complete(self, goal_future)
        goal_handle = goal_future.result()
        if goal_handle is None or not goal_handle.accepted:
            raise RuntimeError("Goal was not accepted")

        self.get_logger().info(f"Goal accepted: order={order}")

        result_future = goal_handle.get_result_async()
        rclpy.spin_until_future_complete(self, result_future)
        result_msg = result_future.result()
        if result_msg is None:
            raise RuntimeError("Failed to get action result")

        return result_msg.status, list(result_msg.result.sequence)


def parse_args() -> int:
    if len(sys.argv) == 2:
        return int(sys.argv[1])
    return 5


def main() -> None:
    order = parse_args()

    rclpy.init()
    node = FibonacciActionClient()

    try:
        status, sequence = node.send_goal(order)
        node.get_logger().info(f"Result status: {status}")
        node.get_logger().info(f"Result sequence: {sequence}")
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == "__main__":
    main()
