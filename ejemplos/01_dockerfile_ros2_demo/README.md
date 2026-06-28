# Ejemplo 01 — Nuestra primera imagen ROS 2 (Dockerfile)

Construimos una imagen con ROS 2 Humble + los nodos de demostración
(`talker` / `listener`) y la corremos. Es el ejemplo del slide *"Creando
nuestro Docker Image"*, listo para ejecutar.

> **Las 3 palabras de hoy:** `Dockerfile` (la receta) → `Image` (la plantilla)
> → `Container` (el programa ejecutándose).

## 1. Construir la imagen (Dockerfile → Image)
Desde esta carpeta:
```bash
docker build -t ros2-humble-demo .
```
- `-t ros2-humble-demo` = nombre ("tag") de la imagen.
- `.` = el "contexto": la carpeta actual, donde está el `Dockerfile`.

Comprueba que se creó:
```bash
docker images | grep ros2-humble-demo
```

## 2. Ejecutar (Image → Container)
```bash
docker run -it --rm ros2-humble-demo
```
- `-it` = interactivo con terminal.
- `--rm` = borra el contenedor al salir (no deja basura).

Ya estás **dentro** del contenedor (verás algo como `root@<id>:~/ros2_ws#`).
ROS ya está sourceado (lo hicimos en el Dockerfile). Lanza el `talker`:
```bash
ros2 run demo_nodes_cpp talker
```
Verás `Publishing: 'Hello World: 1, 2, 3...'`.

## 3. El listener en el MISMO contenedor (segunda terminal)
Mientras el `talker` corre, abre **otra** terminal del host y entra al
contenedor que ya está vivo:
```bash
docker ps                      # copia el NAME o el ID del contenedor
docker exec -it <id> bash      # entra al contenedor en marcha
ros2 run demo_nodes_cpp listener
```
El `listener` imprime `I heard: 'Hello World: ...'`. **Talker y listener se
comunican por DDS dentro del mismo contenedor.**

> 💡 `docker run` crea un contenedor NUEVO; `docker exec` entra a uno que YA
> está corriendo. Es el error más común: lanzar `run` otra vez y preguntarse
> por qué "no se ven" los nodos (¡están en contenedores distintos!).

## 4. Limpieza
Sal de las terminales (`exit` o Ctrl+D). Con `--rm` el contenedor se borra solo.
Para borrar la imagen:
```bash
docker rmi ros2-humble-demo
```

## Idea clave
Esta imagen funciona **igual** en cualquier PC con Docker, sin instalar ROS en
el host. Eso es lo que resuelve Docker: *"works on my machine"* deja de ser un
problema porque **mandas la máquina entera** (la imagen).
