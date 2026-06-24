import rclpy
from rclpy.node import Node

from std_msgs.msg import String


class TrafficLightPublisher(Node):

    def __init__(self):
        super().__init__('traffic_light')
        self.publisher_ = self.create_publisher(String, '/light', 10)
        timer_period = 5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.state = ["RED", "GREEN", "YELLOW"]
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = self.state[self.i]
        self.publisher_.publish(msg)
        self.get_logger().info('Traffic light: "%s"' % msg.data)
        self.i = (self.i + 1) % len(self.state)


def main(args=None):
    rclpy.init(args=args)
    traffic_light = TrafficLightPublisher()
    rclpy.spin(traffic_light)
    traffic_light.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
