from setuptools import find_packages, setup

package_name = 'test_packages'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='fernando',
    maintainer_email='fernando@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            # FORMATO: 'nombre_ejecutable = paquete.archivo:funcion_main'
            'publisher = test_packages.publisher:main',
            'subscriber = test_packages.subscriber:main',
        ],
    },
)
