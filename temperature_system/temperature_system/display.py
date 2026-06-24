import rclpy
from rclpy.node import Node

from std_msgs.msg import String


class DisplaySubscriber(Node):

    def __init__(self):
        super().__init__('display')
        self.subscription = self.create_subscription(
            String,
            '/status',
            self.listener_callback,
            10)
        self.subscription 

    def listener_callback(self, msg):
        self.get_logger().info(f'Resultado final: {msg.data}')


def main(args=None):
    rclpy.init(args=args)
    display = DisplaySubscriber()
    rclpy.spin(display)
    display.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()