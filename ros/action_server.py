import rclpy
from example_interfaces.action import Fibonacci
from rclpy.action import ActionServer
from rclpy.node import Node


def fibonacci_sequence(order: int) -> list[int]:
    if order <= 0:
        return [0]
    if order == 1:
        return [0, 1]

    sequence = [0, 1]
    while len(sequence) <= order:
        sequence.append(sequence[-1] + sequence[-2])
    return sequence


class FibonacciActionServer(Node):
    def __init__(self) -> None:
        super().__init__("fibonacci_action_server")
        self._action_server = ActionServer(
            self,
            Fibonacci,
            "fibonacci",
            self.execute_callback,
        )
        self.get_logger().info("Action ready on /fibonacci")

    def destroy(self) -> None:
        self._action_server.destroy()
        self.destroy_node()

    async def execute_callback(
        self,
        goal_handle,
    ) -> Fibonacci.Result:
        order = goal_handle.request.order
        sequence = fibonacci_sequence(order)

        feedback = Fibonacci.Feedback()
        feedback.sequence = sequence[:-1] if len(sequence) > 1 else sequence
        goal_handle.publish_feedback(feedback)

        result = Fibonacci.Result()
        result.sequence = sequence

        self.get_logger().info(
            f"Handled goal: order={order} sequence={list(result.sequence)}"
        )
        goal_handle.succeed()
        return result


def main() -> None:
    rclpy.init()
    node = FibonacciActionServer()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Stopping action server...")
    finally:
        node.destroy()
        rclpy.try_shutdown()


if __name__ == "__main__":
    main()
