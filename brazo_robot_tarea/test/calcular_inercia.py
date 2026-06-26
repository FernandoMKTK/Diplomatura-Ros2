def calcular_caja():
    print("\n=== INERCIA PARA CAJA ===")
    m = float(input("Masa m [kg]: "))
    x = float(input("Lado x [m]: "))
    y = float(input("Lado y [m]: "))
    z = float(input("Lado z [m]: "))

    ixx = (1 / 12) * m * (y**2 + z**2)
    iyy = (1 / 12) * m * (x**2 + z**2)
    izz = (1 / 12) * m * (x**2 + y**2)

    imprimir_resultado(m, ixx, iyy, izz)


def calcular_cilindro():
    print("\n=== INERCIA PARA CILINDRO ===")
    m = float(input("Masa m [kg]: "))
    r = float(input("Radio r [m]: "))
    h = float(input("Altura h [m]: "))

    ixx = (1 / 12) * m * (3 * r**2 + h**2)
    iyy = ixx
    izz = (1 / 2) * m * r**2

    imprimir_resultado(m, ixx, iyy, izz)


def imprimir_resultado(m, ixx, iyy, izz):
    print("\n=== RESULTADO ===")
    print(f"masa = {m:.4f} kg")
    print(f"ixx  = {ixx:.6f}")
    print(f"iyy  = {iyy:.6f}")
    print(f"izz  = {izz:.6f}")

    print("\nBloque listo para copiar en SDF:\n")
    print(f"""<inertial>
  <mass>{m:.4f}</mass>
  <inertia>
    <ixx>{ixx:.6f}</ixx>
    <iyy>{iyy:.6f}</iyy>
    <izz>{izz:.6f}</izz>
    <ixy>0</ixy>
    <ixz>0</ixz>
    <iyz>0</iyz>
  </inertia>
</inertial>""")


while True:
    print("\nCALCULADORA DE INERCIA")
    print("1. Caja")
    print("2. Cilindro")
    print("3. Salir")

    opcion = input("Elige una opción: ")

    if opcion == "1":
        calcular_caja()
    elif opcion == "2":
        calcular_cilindro()
    elif opcion == "3":
        print("Saliendo...")
        break
    else:
        print("Opción no válida.")