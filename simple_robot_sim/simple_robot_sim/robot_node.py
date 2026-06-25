import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist, TransformStamped
from nav_msgs.msg import Odometry
from tf2_ros import TransformBroadcaster

import math


def quaternion_from_yaw(yaw):
    """
    Convierte el ángulo yaw del robot a un cuaternión.

    En ROS 2, la orientación del robot no se representa directamente como
    un ángulo theta, sino mediante cuaterniones. Esta función recibe el ángulo
    de orientación en el eje Z y devuelve los valores qx, qy, qz y qw.
    """
    qx = 0.0
    qy = 0.0
    qz = math.sin(yaw / 2.0)
    qw = math.cos(yaw / 2.0)
    return qx, qy, qz, qw


class SimpleRobot(Node):
    def __init__(self):
        super().__init__('simple_robot')

        # Suscriptor que recibe comandos de velocidad desde /cmd_vel.
        self.sub = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_callback,
            10
        )
        # Publicador que envía la odometría calculada al tópico /odom.
        self.odom_pub = self.create_publisher(
            Odometry,
            '/odom',
            10
        )

        # Objeto encargado de publicar la transformación odom -> base_link.
        self.tf_broadcaster = TransformBroadcaster(self)

        # Posición inicial del robot en el plano XY.
        self.x = 0.0
        self.y = 0.0

        # Orientación inicial del robot respecto al eje Z.
        self.theta = 0.0
        
        # Velocidad lineal y angular iniciales.
        self.v = 0.0
        self.w = 0.0

        # Guarda el tiempo inicial para calcular el intervalo entre actualizaciones.
        self.last_time = self.get_clock().now()

        # Temporizador que ejecuta la función update cada 0.02 segundos.
        # Esto equivale aproximadamente a una frecuencia de 50 Hz.
        self.timer = self.create_timer(0.02, self.update)

        self.get_logger().info('Nodo simple_robot iniciado')

    def cmd_callback(self, msg):
        """
        Recibe y almacena las velocidades enviadas al robot.

        Esta función se ejecuta cada vez que llega un mensaje Twist al tópico
        /cmd_vel. Extrae la velocidad lineal en X y la velocidad angular en Z,
        que
        """
        # Velocidad lineal hacia adelante o hacia atrás. luego serán usadas para actualizar la posición del robot.

        self.v = msg.linear.x
        # Velocidad angular para girar a la izquierda o derecha.
        self.w = msg.angular.z 

    def update(self):
        """
        Actualiza la posición del robot y publica la odometría.

        Esta función calcula el tiempo transcurrido desde la última actualización,
        integra las velocidades lineal y angular, estima la nueva pose del robot,
        publica el mensaje Odometry y envía la transformación TF correspondiente.
        """
        # Obtiene el tiempo actual del reloj de ROS 2.
        now = self.get_clock().now()

        # Calcula el tiempo transcurrido desde la última actualización.
        dt = (now - self.last_time).nanoseconds / 1e9
        
        
        # Actualiza el tiempo anterior para la siguiente iteración.
        self.last_time = now

        # Actualiza la posición X usando la velocidad lineal y la orientación actual.
        self.x = self.x + self.v*math.cos(self.theta)*dt
        # Actualiza la posición Y usando la velocidad lineal y la orientación actual.
        self.y = self.y + self.v*math.sin(self.theta)*dt
        # Actualiza la orientación del robot usando la velocidad angular.
        self.theta = self.theta + self.w * dt

        # Convierte la orientación theta a cuaternión.
        q = quaternion_from_yaw(self.theta)

        # Crea el mensaje de odometría.
        odom = Odometry()
        # Asigna la marca de tiempo actual.
        odom.header.stamp = now.to_msg()
        # Define el marco de referencia global de la odometría.
        odom.header.frame_id = 'odom'
        # Define el marco móvil asociado al robot.
        odom.child_frame_id = 'base_link'

        # Asigna la posición estimada del robot.
        odom.pose.pose.position.x = self.x
        odom.pose.pose.position.y = self.y
        odom.pose.pose.position.z = 0.0

        # Asigna la orientación estimada del robot en formato cuaternión.
        odom.pose.pose.orientation.x = q[0]
        odom.pose.pose.orientation.y = q[1]
        odom.pose.pose.orientation.z = q[2]
        odom.pose.pose.orientation.w = q[3]

        # Asigna las velocidades actuales del robot.
        odom.twist.twist.linear.x = self.v
        odom.twist.twist.angular.z = self.w

        # Publica el mensaje de odometría en /odom.
        self.odom_pub.publish(odom)

        # Crea el mensaje de transformación TF.
        tf = TransformStamped()
        # Asigna la marca de tiempo actual.
        tf.header.stamp = now.to_msg()
        # Asigna la marca de tiempo actual.
        tf.header.frame_id = 'odom'
        # Define el marco hijo, que corresponde al cuerpo del robot.
        tf.child_frame_id = 'base_link'

        # Asigna la traslación del robot respecto al marco odom.
        tf.transform.translation.x = self.x
        tf.transform.translation.y = self.y
        tf.transform.translation.z = 0.0

        # Asigna la rotación del robot respecto al marco odom.
        tf.transform.rotation.x = q[0]
        tf.transform.rotation.y = q[1]
        tf.transform.rotation.z = q[2]
        tf.transform.rotation.w = q[3]

        # Publica la transformación odom -> base_link.
        self.tf_broadcaster.sendTransform(tf)


def main(args=None):
    rclpy.init(args=args)

    node = SimpleRobot()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
