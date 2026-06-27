from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'robot_sensores_py'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
            (os.path.join('share', package_name, 'launch'), glob('launch/*')),
            (os.path.join('share', package_name, 'worlds'), glob('worlds/*')),
            (os.path.join('share', package_name, 'rviz'), glob('rviz/*.rviz')),
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
            'mover_circulo = robot_sensores_py.mover_circulo:main',
        ],
    },
)
