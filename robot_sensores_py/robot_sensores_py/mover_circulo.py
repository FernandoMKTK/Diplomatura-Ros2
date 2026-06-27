
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class MoverCirculo(Node):
    def __init__(self):
        super().__init__('mover_circulo')

        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)

        # Publica cada 0.1 segundos
        self.timer = self.create_timer(0.1, self.mover)

        self.get_logger().info('Nodo mover_circulo iniciado.')
        self.get_logger().info('Publicando velocidades en /cmd_vel para mover el robot en círculos.')

    def mover(self):
        msg = Twist()

        # Velocidad lineal hacia adelante
        msg.linear.x = 0.3

        # Velocidad angular para girar
        msg.angular.z = 0.6

        # Con estos valores el robot hace un círculo.
        # Radio aproximado = linear.x / angular.z = 0.3 / 0.6 = 0.5 m

        self.publisher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)

    nodo = MoverCirculo()

    try:
        rclpy.spin(nodo)
    except KeyboardInterrupt:
        pass

    # Al cerrar con CTRL+C, detener el robot
    stop_msg = Twist()
    nodo.publisher_.publish(stop_msg)
    nodo.get_logger().info('Robot detenido.')

    nodo.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()