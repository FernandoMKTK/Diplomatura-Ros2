# Tarea — Dale sentidos a tu robot

En clase le pusimos sensores al robot **diferencial** y los conectamos a ROS 2.
Ahora hazlo tú con un robot **omnidireccional** (4 ruedas mecanum), ya armado en
`plantilla_robot_sensores.sdf`. Tú solo completas los 4 `TODO` del `<link
name="chasis">` y luego **puenteas** los sensores a ROS 2.

> Recuerda: **el sensor es nativo de Gazebo; el puente lo lleva a ROS 2.**

## Qué entregar
1. `robot_sensores_<tu_apellido>.sdf` con 4 sensores:
   - **Cámara RGB** (`camera`), **LIDAR 2D** (`gpu_lidar`), **IMU** (`imu`) y
   - **un sensor extra a tu elección** (`depth_camera`, `rgbd_camera`, `gps`,
     `contact`, `force_torque`, `logical_camera`...).
2. El **puente** a ROS 2 (un `bridge_<tu_apellido>.launch.py` o los comandos).
3. **Prueba** de que el dato llega a ROS 2: captura de `rqt_image_view` (cámara)
   + un `ros2 topic echo` del IMU o del sensor extra.
4. **README** de 5 líneas: qué sensor extra elegiste y por qué.

## Requisitos mínimos
- [ ] Los 4 sensores aparecen en `ign topic -l` con la sim corriendo.
- [ ] Cada sensor tiene `<topic>`, `<update_rate>` y `<always_on>`.
- [ ] El IMU lleva `<noise>` gaussiano.
- [ ] `ros2 topic list` muestra tus 4 sensores (el puente funciona).
- [ ] El modelo carga sin errores y el robot no vibra ni se hunde.

## Cómo probarlo
```bash
ign gazebo -r robot_sensores_<tu_apellido>.sdf          # terminal A
# terminal B (antes: source /opt/ros/humble/setup.bash):
ros2 launch ./bridge_<tu_apellido>.launch.py
# terminal C:
ros2 topic list
ros2 run rqt_image_view rqt_image_view
ros2 topic echo /imu
```
Pista del puente (`[` = de Gazebo a ROS): `tópico@tipoROS[tipoGZ`. Los tipos de
cada sensor están en la tabla de `../INTEGRACION_ROS2.md`.

> ⚠️ Sin `-r` Gazebo arranca en pausa y nada publica. Si un sensor no sale en
> `ign topic -l`, revisa que el `<sensor>` esté **dentro** del `<link>`.

## Entrega
Sube el `.sdf`, el `launch` del puente y capturas/video corto.

