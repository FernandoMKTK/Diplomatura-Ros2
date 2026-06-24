#!/usr/bin/env python3
# ============================================================================
#  PUENTE Gazebo (Fortress) <-> ROS 2  para el robot con sensores
# ============================================================================
#  Levanta ros_gz_bridge (parameter_bridge) y conecta de una vez TODOS los
#  tópicos del robot. Así no tienes que escribir el puente sensor por sensor.
#
#  En vez de tipear cada @... a mano, este archivo es el "config/launch" que
#  aparece en las diapositivas de buenas prácticas.
#
#  CÓMO USARLO (con la simulación ya corriendo en otra terminal):
#     ros2 launch puente_sensores.launch.py
#   o, si no lo tienes en un paquete:
#     ros2 launch ./puente_sensores.launch.py
#
#  SINTAXIS de cada argumento del bridge:  <topic>@<tipo_ROS><dir><tipo_GZ>
#     @  = puente bidireccional   (ROS <-> GZ)
#     [  = solo de GAZEBO hacia ROS   (sensores: el dato nace en Gazebo)
#     ]  = solo de ROS hacia GAZEBO   (comandos: /cmd_vel nace en ROS)
#  En Fortress los tipos de Gazebo se escriben "ignition.msgs.*".
# ============================================================================

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='puente_sensores',
        output='screen',
        arguments=[
            # --- Sensores: GAZEBO -> ROS (usan '[') --------------------------
            # Cámara RGB: la imagen.
            # (Nota: en este Fortress, camera_info sale en el tópico FIJO
            #  '/camera_info', no en '/camara/...'. No lo necesitamos para ver
            #  la imagen, así que lo dejamos fuera. Si lo quisieras, añade:
            #  '/camera_info@sensor_msgs/msg/CameraInfo[ignition.msgs.CameraInfo')
            '/camara@sensor_msgs/msg/Image[ignition.msgs.Image',
            # LIDAR 2D: el escaneo láser
            '/escaner@sensor_msgs/msg/LaserScan[ignition.msgs.LaserScan',
            # IMU: aceleración + giro
            '/imu@sensor_msgs/msg/Imu[ignition.msgs.IMU',

            # --- Control: ROS -> GAZEBO ('@' bidireccional, también vale) -----
            '/cmd_vel@geometry_msgs/msg/Twist@ignition.msgs.Twist',

            # --- Reloj de simulación: GAZEBO -> ROS (para usar sim time) ------
            '/clock@rosgraph_msgs/msg/Clock[ignition.msgs.Clock',
        ],
    )

    return LaunchDescription([bridge])
