import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

import sys
import termios
import tty


class KeyboardTeleop(Node):
    """
    Nodo de teleoperación por teclado para controlar un robot en ROS 2.

    Este nodo publica mensajes de tipo Twist en el tópico /cmd_vel.
    Permite mover el robot hacia adelante, atrás, girar a la izquierda,
    girar a la derecha, detenerlo y salir del programa mediante teclas.
    """
    def __init__(self):
        super().__init__('keyboard_teleop')
        self.pub = self.create_publisher(Twist,'cmd_vel',10)

        self.linear_speed = 0.5
        self.angular_speed = 0.8

        self.get_logger().info("""
Control:
  w: avanzar
  s: retroceder
  a: girar izquierda
  d: girar derecha
  x: detener
  q: salir
""")

    def get_key(self):
        """
        Lee una tecla presionada por el usuario sin necesidad de presionar Enter.

        Esta función cambia temporalmente la configuración del terminal para
        capturar una sola tecla de forma inmediata. Luego restaura la configuración
        original del terminal para evitar errores en la consola.
        """
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            key = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return key

    def run(self):
        while rclpy.ok():
            key = self.get_key()
            msg = Twist()

            if key == 'w':
                msg.linear.x = self.linear_speed 

            elif key == 's':
                msg.linear.x = -self.linear_speed 
                
            elif key == 'a':
                msg.angular.z = self.angular_speed
                
            elif key == 'd':
                msg.angular.z = -self.angular_speed

            elif key == 'x':
                msg.linear.x = 0.0 # siempre 0.0 por ser float
                msg.angular.z = 0.0
                
            elif key == 'q':
                break
                
            self.pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = KeyboardTeleop()
    node.run()
    node.destroy_node()
    rclpy.shutdown()
