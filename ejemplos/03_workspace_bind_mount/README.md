# Ejemplo 03 — Workspace montado como volumen (bind mount)

Es el slide *"Docker Volume"*. Montamos el `ros2_ws` del host dentro del
contenedor: compilas **dentro**, pero `build/`, `install/` y `log/` quedan
**en tu disco**. Así no recompilas desde cero cada vez ni pierdes tu código.

> Idea clave: la **imagen** es inmutable; tu **código** vive en el host y entra
> por el volumen. Editas en tu editor de siempre y el contenedor lo ve al
> instante.

Estructura ya incluida:
```
03_workspace_bind_mount/
├── Dockerfile
├── run.sh
└── ros2_ws/
    └── src/mi_paquete/      ← un paquete ROS 2 mínimo (nodo "saludo")
```

## 1. Construir la imagen de desarrollo
```bash
docker build -t ros2-ws-dev .
```

## 2. Entrar con el workspace montado
```bash
./run.sh
```
`run.sh` ejecuta `docker run ... -v "$(pwd)/ros2_ws:/root/ros2_ws"`. El `-v`
(volumen) es lo que conecta la carpeta del host con la del contenedor.

## 3. Compilar DENTRO del contenedor
```bash
colcon build
source install/setup.bash
ros2 run mi_paquete saludo
```
Verás `Publicando: 'Hola desde el workspace montado #1, #2, ...'`.

## 4. La demostración del volumen (el momento "ajá")
1. **Sal** del contenedor (`exit`). En el host, mira tu carpeta:
   ```bash
   ls ros2_ws/
   # build/  install/  log/  src/   ← ¡aparecieron en TU disco!
   ```
2. **Edita en el host** `ros2_ws/src/mi_paquete/mi_paquete/saludo.py`
   (cambia el texto del saludo). No tocas la imagen.
3. Vuelve a entrar (`./run.sh`) y recompila solo lo que cambió:
   ```bash
   colcon build
   source install/setup.bash
   ros2 run mi_paquete saludo
   ```
   Sale tu texto nuevo. **No reconstruiste la imagen** ni recompilaste todo
   desde cero: eso es lo que ahorra el volumen.

## Bind mount vs Named volume
- **Bind mount** (lo de aquí, `-v /ruta/host:/ruta/contenedor`): ideal para
  **desarrollo** — ves y editas los archivos en el host.
- **Named volume** (`-v mis_datos:/ruta`): Docker gestiona el almacenamiento;
  ideal para **datos persistentes** del robot (bagfiles, mapas, modelos). Lo
  usamos en la tarea.

> 💡 Si `build/`/`install/` quedan como `root` en tu host (molesto para
> editar), puedes arreglar permisos con `sudo chown -R $USER ros2_ws` o correr
> el contenedor con tu UID (`--user $(id -u):$(id -g)`). Tema avanzado, no
> imprescindible hoy.
