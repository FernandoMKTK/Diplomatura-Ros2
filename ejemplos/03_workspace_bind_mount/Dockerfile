# ============================================================================
#  EJEMPLO 03 — Imagen de DESARROLLO con colcon (para usar con bind mount)
# ============================================================================
#  Trae ROS 2 Humble + colcon (para compilar workspaces). La idea es montar el
#  workspace del host como VOLUMEN, así compilas dentro del contenedor pero los
#  resultados quedan en tu disco (no se pierden y no recompilas cada vez).
#
#  CONSTRUIR:  docker build -t ros2-ws-dev .
#  EJECUTAR:   ./run.sh   (monta ./ros2_ws del host)
# ============================================================================
FROM ros:humble

ENV DEBIAN_FRONTEND=noninteractive

# colcon (para compilar) + un paquete de demo extra por comodidad.
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3-colcon-common-extensions \
        ros-humble-demo-nodes-py \
    && rm -rf /var/lib/apt/lists/*

SHELL ["/bin/bash", "-c"]

# Sourcear ROS y, si existe, el workspace ya compilado (para usar `ros2 run`).
RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc && \
    echo "[ -f /root/ros2_ws/install/setup.bash ] && source /root/ros2_ws/install/setup.bash" >> ~/.bashrc

WORKDIR /root/ros2_ws
CMD ["bash"]
