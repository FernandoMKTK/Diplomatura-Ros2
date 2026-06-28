# PLANTILLA — Completa los TODO. Construye una imagen ROS 2 que pueda:
#   - correr los nodos demo (talker / listener)
#   - grabar bags con `ros2 bag`
FROM ros:humble-ros-core

ENV DEBIAN_FRONTEND=noninteractive

# TODO: instala los paquetes necesarios en UN solo RUN y limpia la cache de apt.
#   Pistas (nombres de paquetes apt):
#     - ros-humble-demo-nodes-cpp                    (talker / listener)
#     - ros-humble-ros2bag                           (el comando `ros2 bag`)
#     - ros-humble-rosbag2-storage-default-plugins   (almacenamiento del bag)
# RUN apt-get update && apt-get install -y --no-install-recommends \
#         ... \
#     && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y --no-install-recommends \
        ros-humble-demo-nodes-cpp \
        ros-humble-ros2bag \
        ros-humble-rosbag2-storage-default-plugins \
    && rm -rf /var/lib/apt/lists/*

CMD ["bash"]
