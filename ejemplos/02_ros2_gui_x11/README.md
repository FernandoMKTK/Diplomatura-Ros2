# Ejemplo 02 — ROS 2 con interfaz gráfica (RViz / Gazebo) en Docker

Un contenedor no tiene pantalla. Para ver **RViz** o **Gazebo** hay que
prestarle el servidor gráfico **X11** del host. Es el slide *"ROS2 dentro de
Docker"*, paso a paso.

> Regla mental: el contenedor "dibuja" pero la **ventana** la pone el host. Le
> pasamos (1) la variable `DISPLAY`, (2) el socket de X11, y (3) permiso con
> `xhost`.

## 1. Descargar una imagen con GUI (desktop-full trae RViz y Gazebo)
```bash
docker pull osrf/ros:humble-desktop-full
```
> ⚠️ Es pesada (~3–4 GB). Si solo necesitas RViz, `humble-desktop` basta.

## 2. Dar permiso al contenedor para usar tu pantalla
```bash
xhost +local:docker
```
> Esto abre X11 a contenedores locales. Al terminar la clase puedes cerrarlo
> con `xhost -local:docker`.

## 3. Ejecutar el contenedor con acceso gráfico

### Caso A — GPU Intel / AMD, o sin GPU dedicada
```bash
docker run -it \
  --name ros_gui \
  --env="DISPLAY=$DISPLAY" \
  --env="QT_X11_NO_MITSHM=1" \
  --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
  --device /dev/dri:/dev/dri \
  osrf/ros:humble-desktop-full bash
```

### Caso B — GPU NVIDIA (requiere nvidia-container-toolkit)
```bash
docker run -it --gpus all \
  -e DISPLAY=$DISPLAY \
  -e QT_X11_NO_MITSHM=1 \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  osrf/ros:humble-desktop-full bash
```

**Qué hace cada flag:**
| Flag | Para qué |
|---|---|
| `--env DISPLAY=$DISPLAY` | le dice al contenedor a qué pantalla dibujar |
| `-v /tmp/.X11-unix:...` | comparte el socket de X11 (el "cable" a la pantalla) |
| `QT_X11_NO_MITSHM=1` | evita un fallo común de memoria compartida con Qt |
| `--device /dev/dri` | aceleración gráfica por GPU Intel/AMD |
| `--gpus all` | expone la GPU NVIDIA al contenedor |

## 4. Probar la GUI (dentro del contenedor)
```bash
source /opt/ros/humble/setup.bash   # en desktop-full no está en ~/.bashrc
rviz2
```
Debe abrirse la ventana de **RViz** en tu escritorio. Para Gazebo:
```bash
ign gazebo            # o 'gazebo' según la versión incluida
```

## 5. Volver a entrar a ese contenedor
Como NO usamos `--rm`, el contenedor `ros_gui` sigue existiendo:
```bash
docker start ros_gui            # arráncalo si estaba detenido
docker exec -it ros_gui bash    # entra otra vez
```

## Errores típicos
| Síntoma | Causa | Arreglo |
|---|---|---|
| `cannot open display` | falta permiso X11 | corre `xhost +local:docker` |
| Ventana negra / no abre | `DISPLAY` mal pasado | revisa `echo $DISPLAY` en el host |
| RViz muy lento | sin aceleración GPU | añade `--device /dev/dri` (Intel/AMD) |
| `command not found: rviz2` | ROS sin sourcear | `source /opt/ros/humble/setup.bash` |
