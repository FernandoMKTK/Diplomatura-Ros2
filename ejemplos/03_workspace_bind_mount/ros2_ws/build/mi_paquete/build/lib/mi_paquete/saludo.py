import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class Saludo(Node):
    """Publica un saludo cada segundo. Edítalo en el host y recompila:
    verás el cambio sin reconstruir la imagen (esa es la gracia del volumen)."""

    def __init__(self):
        super().__init__('saludo')
        self.pub = self.create_publisher(String, 'saludo', 10)
        self.timer = self.create_timer(1.0, self.tick)
        self.n = 0

    def tick(self):
        self.n += 1
        msg = String()
        msg.data = f'Hola desde el workspace montado MODIFICADO #{self.n}'
        self.pub.publish(msg)
        self.get_logger().info(f'Publicando: {msg.data}')


def main():
    rclpy.init()
    nodo = Saludo()
    try:
        rclpy.spin(nodo)
    except KeyboardInterrupt:
        pass
    finally:
        nodo.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
