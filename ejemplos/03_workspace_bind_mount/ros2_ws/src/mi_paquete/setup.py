from setuptools import setup

package_name = 'mi_paquete'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='alumno',
    maintainer_email='alumno@example.com',
    description='Paquete mínimo para demostrar bind mounts (volúmenes) en Docker',
    license='MIT',
    entry_points={
        'console_scripts': [
            'saludo = mi_paquete.saludo:main',
        ],
    },
)
