# Tarea — Tu primer robot en SDF (Gazebo Fortress)

## Contexto
En clase construimos juntos un **robot móvil diferencial** que se desplaza por
el suelo (`ejemplo_robot_diferencial.sdf`). Ahora te toca a ti, pero con un
**tipo de robot y una tarea diferentes**: un **brazo robótico anclado** cuyas
**articulaciones** se mueven.

El objetivo es que practiques la anatomía de un archivo **SDF**: `model`,
`link`, `inertial`, `collision`, `visual` y `joint`.

## Qué debes entregar
Un archivo SDF llamado `brazo_robot_<tu_apellido>.sdf` con un **brazo robótico
de 2 grados de libertad (2 GDL)**:

1. **`base`** — link anclado al mundo (con joint `fixed`).
2. **`eslabon_1`** — unido a la base por un joint **`revolute`** con límites.
3. **`eslabon_2`** — unido al eslabón 1 por otro joint **`revolute`** con límites.
4. **Control de las articulaciones** — el brazo debe **moverse** cuando se le
   ordena un ángulo por tópico (plugin `JointPositionController`).

Parte de la plantilla `plantilla_brazo_robot.sdf`: el mundo (física, luz,
suelo y sistemas) ya está hecho; tú completas los `TODO` del modelo.

## Requisitos mínimos
- [ ] Cada link tiene `<inertial>` (masa + inercia **coherentes**, no cero).
- [ ] Cada link tiene `<visual>` **y** `<collision>` con geometría consistente.
- [ ] Los dos joints son `revolute` y tienen `<limit>` realistas (no infinitos).
- [ ] **Cada joint tiene su `JointPositionController`** y responde a un comando
      de ángulo (el brazo se mueve, no solo "se ve").
- [ ] El modelo **carga sin errores** y se ve bien posado en Gazebo.
- [ ] Comentarios en español explicando **al menos** un link y un joint.

## Sobre el controlador (`JointPositionController`)
Para que el brazo se mueva necesitas un **plugin** por articulación: el
`JointPositionController`. Le envías un **ángulo deseado** por un tópico y él se
encarga de llevar la junta hasta ahí y mantenerla (mediante un PID). Por ahora
basta con añadirlo y comprobar que el brazo responde; **veremos en detalle cómo
funciona este controlador en una clase posterior**.

## Cómo probarlo
```bash
ign gazebo brazo_robot_<tu_apellido>.sdf
```
El brazo debe aparecer de pie sobre el suelo, sin colapsar ni vibrar.

> ⚠️ Gazebo arranca **EN PAUSA**: pulsa ▶ (Play) o lanza con `ign gazebo -r ...`,
> si no, los comandos no mueven nada.

Mover las articulaciones (en otra terminal, con la sim en marcha). El nombre del
tópico sigue el patrón `/model/<modelo>/joint/<junta>/0/cmd_pos`:
```bash
ign topic -t "/model/brazo/joint/junta_1/0/cmd_pos" \
          -m ignition.msgs.Double -p "data: 1.0"
ign topic -t "/model/brazo/joint/junta_2/0/cmd_pos" \
          -m ignition.msgs.Double -p "data: -0.8"
```
Ambas articulaciones deben moverse al ángulo indicado y mantenerse ahí.

## Pista clave: la inercia
Para una **caja** de lados `(x, y, z)` y masa `m`:

```
ixx = (1/12)·m·(y² + z²)
iyy = (1/12)·m·(x² + z²)
izz = (1/12)·m·(x² + y²)
```

Para un **cilindro** de radio `r`, altura `h` y masa `m` (eje en Z):

```
ixx = iyy = (1/12)·m·(3r² + h²)
izz = (1/2)·m·r²
```

## Rúbrica (20 pts)
| Criterio | Pts |
|---|---|
| Estructura SDF válida y carga sin errores | 4 |
| Links completos (inertial + visual + collision) | 6 |
| Joints revolute correctos, con eje y límites | 4 |
| Control: las articulaciones se mueven por tópico | 6 |


## Entrega
Sube el archivo `.sdf` y un pequeño video del brazo moviéndose en Gazebo.
