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

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def remove_snap_paths(path_value):
    return os.pathsep.join(
        path for path in path_value.split(os.pathsep)
        if path and not path.startswith('/snap/')
        and '/snap/' not in path
    )


def clean_rviz_environment():
    env = {}
    path_variables = [
        'GDK_PIXBUF_MODULEDIR',
        'GIO_MODULE_DIR',
        'GSETTINGS_SCHEMA_DIR',
        'GTK_EXE_PREFIX',
        'GTK_PATH',
        'LD_LIBRARY_PATH',
        'LOCPATH',
        'PATH',
        'SNAP_LIBRARY_PATH',
        'XDG_DATA_DIRS',
        'XDG_DATA_HOME',
    ]

    for variable in path_variables:
        env[variable] = remove_snap_paths(os.environ.get(variable, ''))

    for variable in os.environ:
        if variable.startswith('SNAP') or variable.startswith('GTK_'):
            env.setdefault(variable, '')

    env['GDK_PIXBUF_MODULE_FILE'] = ''
    env['GTK_IM_MODULE_FILE'] = ''
    return env


def generate_launch_description():
    rviz_file = os.path.join(
        get_package_share_directory('robot_sensores_py'),
        'rviz',
        'robot_diferencial.rviz'
    )

    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='bridge_Munoz',
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

            # depth_camera: Camara de profundidad
            '/depth_camera@sensor_msgs/msg/Image[ignition.msgs.Image',
            
            # GPS
            '/gps/fix@sensor_msgs/msg/NavSatFix[ignition.msgs.NavSat',

            # --- Reloj de simulación: GAZEBO -> ROS (para usar sim time) ------
            '/clock@rosgraph_msgs/msg/Clock[ignition.msgs.Clock',
        ],
    )

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_file],
        additional_env=clean_rviz_environment(),
    )

    return LaunchDescription([
        bridge,
        rviz,
    ])
