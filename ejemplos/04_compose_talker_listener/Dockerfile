# Imagen mínima para el demo de Compose: ROS 2 Humble + nodos de demostración.
FROM ros:humble-ros-core

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
        ros-humble-demo-nodes-cpp \
    && rm -rf /var/lib/apt/lists/*

# La imagen base ros:humble-* ya trae un ENTRYPOINT (ros_entrypoint.sh) que
# hace `source /opt/ros/humble/setup.bash` antes de ejecutar el comando.
# Por eso en docker-compose.yml podemos poner `command: ros2 run ...`
# directamente: ROS ya queda disponible.
CMD ["bash"]
