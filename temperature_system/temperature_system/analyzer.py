import rclpy
from rclpy.node import Node

from std_msgs.msg import String, Int32


class AnalyzerNode(Node):

    def __init__(self):
        super().__init__('analyzer')
        # Suscrpcion al topico /temperature
        self.subscription = self.create_subscription(
            Int32,
            '/temperature',
            self.listener_callback,
            10)
        self.subscription  

        # Publicacion al topico /status
        self.publisher_ = self.create_publisher(String, '/status', 10)
        self.i =1

    def listener_callback(self, msg):
        temperatura = msg.data

        if temperatura < 18:
            estado = "Frio"
        elif 18 <= temperatura < 28:
            estado = "Agradable"
        else:
            estado = "Calor"

        estado_msg = String()
        estado_msg.data = estado
        self.publisher_.publish(estado_msg)

        self.get_logger().info(
            f'Procesamiento {self.i}: {temperatura} °C -> {estado}'
        )

        self.i += 1

def main(args=None):
    rclpy.init(args=args)
    analyzer = AnalyzerNode()
    rclpy.spin(analyzer)
    analyzer.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
