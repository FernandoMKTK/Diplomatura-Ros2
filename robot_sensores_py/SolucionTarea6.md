## Sensor Escogido

### Cámara de profundidad

Se eligió una cámara de profundidad porque permite medir la distancia entre el robot y los objetos del entorno.
Este sensor es útil en navegación autónoma porque ayuda al robot a detectar obstáculos cercanos.
A diferencia de una cámara RGB, no solo entrega color, sino también información de distancia.
Con estos datos, el robot puede tomar mejores decisiones para evitar choques durante su recorrido.

### GPS
Adicionalmente, se agregó un sensor GPS para obtener la posición global simulada del robot.
Este sensor permite conocer la ubicación aproximada del robot dentro de un sistema de coordenadas geográficas.
En navegación autónoma, el GPS es útil para seguir rutas, definir puntos de destino y estimar desplazamientos.
Por ello, el GPS ayuda al robot a orientarse mejor cuando debe desplazarse hacia una posición determinada.

## FUENTES DE CODIGO USADO:

https://automaticaddison.com/how-to-add-a-depth-camera-to-an-sdf-file-for-gazebo/

https://docs-nav2-org.translate.goog/tutorials/docs/navigation2_with_gps.html?_x_tr_sl=en&_x_tr_tl=es&_x_tr_hl=es&_x_tr_pto=tc

### LINK DEL REPOSITORIO DEL CURSO

https://github.com/FernandoMKTK/Diplomatura-Ros2.git


```text
robot_sensores_py/
├── launch
│   ├── bridge_Munoz.launch.py
│   └── puente_sensores.launch.py
├── package.xml
├── resource
│   └── robot_sensores_py
├── robot_sensores_py
│   ├── __init__.py
│   ├── mover_circulo.py
│   └── __pycache__
│       ├── __init__.cpython-310.pyc
│       └── mover_circulo.cpython-310.pyc
├── rviz
│   └── robot_diferencial.rviz
├── setup.cfg
├── setup.py
├── SolucionTarea6.md
├── TAREA.md
```
