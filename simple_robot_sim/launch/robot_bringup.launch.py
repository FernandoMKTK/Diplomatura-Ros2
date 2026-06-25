from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='simple_robot_sim',
            executable='fake_lidar_node',
            name='lidar',
        ),
        Node(
            package='simple_robot_sim',
            executable='keyboard_node',
            name='teclado',
            prefix='xterm -e',
            output='screen',
        ),
        Node(
            package='simple_robot_sim',
            executable='robot_node',
            name='robot',
        ),
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='base_to_camera_tf',
            arguments=[
                '0.20', '0.0', '0.30',
                '-1.5708', '0.0', '-1.5708',
                'base_link',
                'camera_link'
            ],
        ),
        Node(
            package='simple_robot_sim',
            executable='webcam_node',
            name='camara',
        ),
        Node(
            package='simple_robot_sim',
            executable='webcam3D_node',
            name='camara_3d',
        ),

        
    ])
