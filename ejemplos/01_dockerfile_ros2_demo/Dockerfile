# ============================================================================
#  EJEMPLO DE CLASE — Nuestra primera imagen ROS 2
# ============================================================================
#  "La receta": este Dockerfile construye una IMAGEN con ROS 2 Humble y los
#  nodos de demostración (talker / listener) ya instalados y listos para usar.
#
#  Cada instrucción es una CAPA. Docker las cachea: si no cambias una línea,
#  no la vuelve a ejecutar. Por eso el orden importa (lo que cambia poco va
#  arriba; lo que cambia mucho, abajo).
#
#  CONSTRUIR:   docker build -t ros2-humble-demo .
#  EJECUTAR:    docker run -it --rm ros2-humble-demo
# ============================================================================

# 1) Imagen BASE: ROS 2 Humble mínimo (solo el core, pesa poco).
FROM ros:humble-ros-core

# 2) Que apt no pida confirmaciones durante el build (build no interactivo).
ENV DEBIAN_FRONTEND=noninteractive

# 3) Instalar los nodos de demostración de ROS (talker en C++ y en Python).
#    Juntamos update + install + limpieza en UN solo RUN para no dejar
#    capas intermedias pesadas. Al final borramos la cache de apt.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ros-humble-demo-nodes-cpp \
        ros-humble-demo-nodes-py \
        locales \
    && rm -rf /var/lib/apt/lists/*

# 4) Configurar locales (evita errores de codificación Unicode en ROS).
RUN locale-gen en_US en_US.UTF-8 && \
    update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

# 5) Que ROS quede "sourceado" automáticamente cada vez que se abra una bash.
#    Así dentro del contenedor ya puedes usar `ros2` sin sourcear a mano.
SHELL ["/bin/bash", "-c"]
RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc

# 6) Carpeta de trabajo por defecto: el workspace de ROS 2.
WORKDIR /root/ros2_ws

# 7) Crear la carpeta src del workspace (donde irían tus paquetes).
RUN mkdir -p src

# 8) Comando por defecto al arrancar el contenedor: abrir una bash.
CMD ["bash"]
