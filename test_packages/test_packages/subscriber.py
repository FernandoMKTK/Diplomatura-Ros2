import rclpy
from rclpy.node import Node

from std_msgs.msg import Int32 


class VelocitySubscriber(Node):

    def __init__(self):
        super().__init__('velocity_subscriber')      

        self.subscription = self.create_subscription(
            Int32,                  
            'velocidad',           
            self.listener_callback,
            10
        )
        self.subscription 

    def listener_callback(self, msg):
        resultado = msg.data * 10    
        self.get_logger().info(f'Recibido: {msg.data} → x10 = {resultado}')


def main(args=None):
    rclpy.init(args=args)
    subscriber = VelocitySubscriber()
    rclpy.spin(subscriber)
    subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()