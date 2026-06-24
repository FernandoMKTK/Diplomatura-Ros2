import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class CarSubscriber(Node):

    def __init__(self):
        super().__init__('car')
        self.subscription = self.create_subscription(
            String,
            '/light',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    

    def listener_callback(self, msg):
        if msg.data == "RED":
            action = "Detenerse"
        elif msg.data == "GREEN":
            action = "Avanzar"
        elif msg.data == "YELLOW":
            action = "Precaución"
        else:
            action = "Estado desconocido"
        self.get_logger().info(f'{msg.data} -> {action}')

def main(args=None):
    rclpy.init(args=args)
    car = CarSubscriber()
    rclpy.spin(car)
    car.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()