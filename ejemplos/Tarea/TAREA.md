# Tarea — Tu mini-arquitectura ROS 2 en contenedores

En clase levantamos dos contenedores (talker + listener) con Compose. Ahora
arma una pequeña **arquitectura de robot**: tres contenedores en una red, y un
**volumen** que guarda una grabación. Junta las tres ideas del pipeline:
**Dockerfile + Compose (red) + Volumen**.

Parte de la carpeta `plantilla/` y completa los `TODO`.

## Qué entregar
1. `Dockerfile` que instale: nodos demo + `ros2 bag` + almacenamiento de bags.
2. `docker-compose.yml` con **tres servicios** en una red `robot_net`:
   - `talker` (ya dado) → publica `/chatter`
   - `listener` → se suscribe a `/chatter`
   - `grabador` → graba `/chatter` con `ros2 bag` en un **volumen** `bags_volume`

## Requisitos mínimos
- [ ] La imagen construye sin errores (`docker compose build`).
- [ ] `docker compose up` levanta los 3 contenedores.
- [ ] El `listener` imprime `I heard:` (hay comunicación entre contenedores).
- [ ] El bag queda en el **volumen** y persiste tras `docker compose down`.
- [ ] Los 3 servicios comparten red y `ROS_DOMAIN_ID`.

## Cómo probarlo
```bash
cd Tarea
docker compose up                 # déjalo ~10 s y Ctrl+C
docker compose down               # NO borres el volumen

# El bag sobrevivió en el volumen:
docker volume ls | grep bags_volume
docker run --rm -v bags_volume:/bags tarea-ros2 \
  bash -c "ros2 bag info /bags/sesion"
```

> 💡 Pistas: `command:` en compose funciona sin sourcear ROS (el entrypoint de
> `ros:humble-*` ya lo hace). Si el `listener` no oye nada, prueba
> `network_mode: host` en los servicios. Los tipos/comandos están en
> `../COMANDOS_DOCKER.md`.

## Entrega
Sube `Dockerfile`, `docker-compose.yml`.
