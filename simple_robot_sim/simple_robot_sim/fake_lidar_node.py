import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan

import math
import random


class FakeLidar(Node):
    def __init__(self):
        super().__init__('fake_lidar')

        self.pub = self.create_publisher(LaserScan, '/scan', 10)
        self.timer = self.create_timer(0.1, self.publish_scan)  # 10 Hz

        self.angle_min = -math.pi
        self.angle_max = math.pi
        self.num_readings = 360
        self.angle_increment = (self.angle_max - self.angle_min) / self.num_readings

        self.range_min = 0.12
        self.range_max = 6.0

    def publish_scan(self):
        msg = LaserScan()

        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'base_link'

        msg.angle_min = self.angle_min
        msg.angle_max = self.angle_max
        msg.angle_increment = self.angle_increment

        msg.time_increment = 0.0
        msg.scan_time = 0.1

        msg.range_min = self.range_min
        msg.range_max = self.range_max

        ranges = []

        for i in range(self.num_readings):
            distance = random.uniform(1.0, self.range_max)

            # Simula algunos obstáculos cercanos
            if 80 < i < 110:
                distance = random.uniform(0.5, 1.2)

            if 230 < i < 260:
                distance = random.uniform(0.8, 1.5)

            ranges.append(distance)

        msg.ranges = ranges
        msg.intensities = [0.0] * self.num_readings

        self.pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = FakeLidar()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
