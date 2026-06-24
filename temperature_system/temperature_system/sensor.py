import rclpy
from rclpy.node import Node
import random
from std_msgs.msg import Int32

class SensorPublisher(Node):

    def __init__(self):
        super().__init__('sensor')
        self.publisher_ = self.create_publisher(Int32, '/temperature', 10)
        timer_period = 1  # second
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 1

    def timer_callback(self):
        msg = Int32()
        msg.data = random.choice(range(15, 36)) # Da un valor aleatorio dentro de un rango definido 15-35
        self.publisher_.publish(msg)
        self.get_logger().info(f'Lectura {self.i}: temperatura = {msg.data} °C')
        self.i += 1


def main(args=None):
    rclpy.init(args=args)

    sensor = SensorPublisher()
    rclpy.spin(sensor)
    sensor.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()