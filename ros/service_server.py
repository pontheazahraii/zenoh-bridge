import rclpy
from example_interfaces.srv import AddTwoInts
from rclpy.node import Node


class AddTwoIntsServer(Node):
    def __init__(self) -> None:
        super().__init__("add_two_ints_server")
        self.create_service(AddTwoInts, "add_two_ints", self.handle_request)
        self.get_logger().info("Service ready on /add_two_ints")

    def handle_request(
        self,
        request: AddTwoInts.Request,
        response: AddTwoInts.Response,
    ) -> AddTwoInts.Response:
        response.sum = request.a + request.b
        self.get_logger().info(
            f"Handled request: {request.a} + {request.b} = {response.sum}"
        )
        return response


def main() -> None:
    rclpy.init()
    node = AddTwoIntsServer()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Stopping service server...")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
