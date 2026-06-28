#!/usr/bin/env bash
# ============================================================================
#  Corre el contenedor de desarrollo montando ./ros2_ws del host como VOLUMEN.
#  Lo que compiles (build/ install/ log/) aparece EN TU DISCO y persiste.
# ============================================================================
cd "$(dirname "$0")"

docker run -it --rm \
  --name ws_dev \
  -v "$(pwd)/ros2_ws:/root/ros2_ws" \
  ros2-ws-dev
