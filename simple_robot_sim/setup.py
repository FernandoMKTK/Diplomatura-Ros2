from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'simple_robot_sim'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
            (os.path.join('share', package_name, 'launch'), glob('launch/*')),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='fernando',
    maintainer_email='a20196303@pucp.edu.pe',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'robot_node = simple_robot_sim.robot_node:main',
            'keyboard_node = simple_robot_sim.keyboard_node:main',
            'fake_lidar_node = simple_robot_sim.fake_lidar_node:main',
            'webcam_node = simple_robot_sim.webcam_node:main',
            'webcam3D_node = simple_robot_sim.webcam3D_node:main',
        ],
    },
)
