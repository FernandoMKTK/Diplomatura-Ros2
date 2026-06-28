# Ejemplo 04 (NUEVO) — Multi-contenedor con Docker Compose + red

> Este ejemplo **no está como código en el PDF**: el deck explica Compose y
> Networks en concepto, y aquí los juntamos en un archivo que corre de verdad.

Dos contenedores ROS 2 (un `talker` y un `listener`) que se descubren y se
comunican por **DDS** a través de una **red Docker** compartida — todo con un
solo comando. Es la versión mínima de una arquitectura robótica multi-contenedor
(percepción / navegación / control en contenedores separados).

## Levantar todo
```bash
docker compose up
```
La primera vez construye la imagen y arranca ambos contenedores. Verás
**intercaladas** las dos salidas:
```
talker    | [INFO] Publishing: 'Hello World: 1'
listener  | [INFO] I heard: 'Hello World: 1'
talker    | [INFO] Publishing: 'Hello World: 2'
listener  | [INFO] I heard: 'Hello World: 2'
```
Que el `listener` (un contenedor) reciba lo del `talker` (otro contenedor)
**prueba** que la red Docker + el mismo `ROS_DOMAIN_ID` permiten la
comunicación ROS 2 entre contenedores.

## Apagar todo
`Ctrl+C` y luego:
```bash
docker compose down        # detiene y borra contenedores + la red
```

## Cosas para mostrar en vivo
- **Ver la red creada:**
  ```bash
  docker network ls | grep ros_net
  ```
- **Aislamiento por dominio:** cambia el `ROS_DOMAIN_ID` de `listener` a `7`,
  `docker compose up` otra vez → el listener **deja de oír** (están en dominios
  distintos, como dos proyectos que no se interfieren).
- **Escalar:** `docker compose up --scale listener=3` → tres listeners oyendo al
  mismo talker.
- **En segundo plano:** `docker compose up -d` y luego `docker compose logs -f`.

## Si el listener NO oye nada (plan B)
En algunas máquinas el descubrimiento DDS por multicast en redes bridge falla.
Solución a prueba de balas en Linux: usa la **red del host** (quita el bloque
`networks` y pon `network_mode: host` en cada servicio). Comparten la red del
host y el descubrimiento siempre funciona:
```yaml
services:
  talker:
    image: ros2-compose-demo
    network_mode: host
    environment:
      - ROS_DOMAIN_ID=42
    command: ros2 run demo_nodes_cpp talker
  listener:
    image: ros2-compose-demo
    network_mode: host
    environment:
      - ROS_DOMAIN_ID=42
    command: ros2 run demo_nodes_cpp listener
```

## Por qué esto importa (conexión con el caso industrial del PDF)
En la fábrica del slide final, cada robot/PC corre sus nodos ROS 2 en
contenedores. Compose es lo que te deja **describir toda esa arquitectura en un
archivo** y desplegarla igual en el laboratorio y en producción.
