#!/usr/bin/env python3

import argparse
import math
import os
import numpy as np
import open3d as o3d


def parse_vec(text):
    values = text.replace(",", " ").split()
    if len(values) != 3:
        raise ValueError("Debes ingresar 3 valores, por ejemplo: '0 0 0'")
    return np.array([float(v) for v in values], dtype=float)


def rpy_to_matrix(roll, pitch, yaw):
    cr = math.cos(roll)
    sr = math.sin(roll)
    cp = math.cos(pitch)
    sp = math.sin(pitch)
    cy = math.cos(yaw)
    sy = math.sin(yaw)

    rx = np.array([
        [1, 0, 0],
        [0, cr, -sr],
        [0, sr, cr]
    ])

    ry = np.array([
        [cp, 0, sp],
        [0, 1, 0],
        [-sp, 0, cp]
    ])

    rz = np.array([
        [cy, -sy, 0],
        [sy, cy, 0],
        [0, 0, 1]
    ])

    return rz @ ry @ rx


def matrix_to_rpy(R):
    pitch = math.atan2(
        -R[2, 0],
        math.sqrt(R[0, 0] ** 2 + R[1, 0] ** 2)
    )

    if abs(math.cos(pitch)) > 1e-9:
        roll = math.atan2(R[2, 1], R[2, 2])
        yaw = math.atan2(R[1, 0], R[0, 0])
    else:
        roll = 0.0
        yaw = math.atan2(-R[0, 1], R[1, 1])

    return roll, pitch, yaw


def make_transform(xyz, rpy):
    T = np.eye(4)
    T[:3, :3] = rpy_to_matrix(rpy[0], rpy[1], rpy[2])
    T[:3, 3] = xyz
    return T


def transform_points(points, T):
    points_h = np.hstack([points, np.ones((points.shape[0], 1))])
    transformed = (T @ points_h.T).T
    return transformed[:, :3]


def load_surface_points(mesh_path, samples):
    mesh_path = os.path.expanduser(mesh_path)

    mesh = o3d.io.read_triangle_mesh(mesh_path)

    if mesh.is_empty():
        raise RuntimeError(f"No se pudo cargar la malla: {mesh_path}")

    mesh.compute_vertex_normals()

    pcd = mesh.sample_points_uniformly(number_of_points=samples)

    points = np.asarray(pcd.points)

    if points.shape[0] == 0:
        raise RuntimeError(f"No se generaron puntos desde la malla: {mesh_path}")

    return pcd, points


def pick_ring_points(mesh_path, title, feature_index, min_points, samples):
    pcd, points = load_surface_points(mesh_path, samples)

    print("\n====================================================")
    print(title)
    print(f"Referencia circular / agujero {feature_index}")
    print("====================================================")
    print(f"Malla: {mesh_path}")
    print(f"Selecciona por lo menos {min_points} puntos SOBRE EL MISMO BORDE CIRCULAR.")
    print("NO selecciones el centro.")
    print("NO mezcles borde exterior con borde interior.")
    print("Usa SHIFT + clic izquierdo para seleccionar puntos.")
    print("Cuando termines, presiona Q.")
    print("====================================================\n")

    vis = o3d.visualization.VisualizerWithEditing()
    vis.create_window(window_name=f"{title} - agujero {feature_index}", width=1200, height=800)
    vis.add_geometry(pcd)
    vis.run()
    picked_indices = vis.get_picked_points()
    vis.destroy_window()

    if len(picked_indices) < min_points:
        raise RuntimeError(
            f"Seleccionaste {len(picked_indices)} puntos. "
            f"Debes seleccionar al menos {min_points} puntos del borde."
        )

    picked = points[picked_indices]

    return picked


def fit_circle_3d(points):
    centroid = np.mean(points, axis=0)
    centered = points - centroid

    _, _, vt = np.linalg.svd(centered)

    u = vt[0]
    v = vt[1]
    normal = vt[2]

    x = centered @ u
    y = centered @ v

    A = np.column_stack([x, y, np.ones_like(x)])
    b = -(x ** 2 + y ** 2)

    sol, _, _, _ = np.linalg.lstsq(A, b, rcond=None)

    D = sol[0]
    E = sol[1]
    F = sol[2]

    cx = -D / 2.0
    cy = -E / 2.0

    radius = math.sqrt(max(0.0, (D ** 2 + E ** 2) / 4.0 - F))

    center_3d = centroid + cx * u + cy * v

    return center_3d, normal, radius


def collect_hole_centers(mesh_path, title, features, min_points, samples):
    centers = []

    for i in range(1, features + 1):
        ring_points = pick_ring_points(
            mesh_path=mesh_path,
            title=title,
            feature_index=i,
            min_points=min_points,
            samples=samples
        )

        center, normal, radius = fit_circle_3d(ring_points)

        print("\nCentro calculado:")
        print(f"center = {center[0]:.6f} {center[1]:.6f} {center[2]:.6f}")
        print(f"radius = {radius:.6f}")
        print("")

        centers.append(center)

    return np.array(centers)


def best_fit_transform(child_points, parent_points):
    child_centroid = np.mean(child_points, axis=0)
    parent_centroid = np.mean(parent_points, axis=0)

    child_centered = child_points - child_centroid
    parent_centered = parent_points - parent_centroid

    H = child_centered.T @ parent_centered

    U, _, Vt = np.linalg.svd(H)
    R = Vt.T @ U.T

    if np.linalg.det(R) < 0:
        Vt[-1, :] *= -1
        R = Vt.T @ U.T

    t = parent_centroid - R @ child_centroid

    T = np.eye(4)
    T[:3, :3] = R
    T[:3, 3] = t

    return T


def preview_result(parent_mesh_path, child_mesh_path, T_parent_visual, T_child_visual, T_parent_child):
    parent_mesh = o3d.io.read_triangle_mesh(os.path.expanduser(parent_mesh_path))
    child_mesh = o3d.io.read_triangle_mesh(os.path.expanduser(child_mesh_path))

    parent_mesh.compute_vertex_normals()
    child_mesh.compute_vertex_normals()

    parent_mesh.transform(T_parent_visual)
    child_mesh.transform(T_parent_child @ T_child_visual)

    parent_mesh.paint_uniform_color([0.7, 0.7, 0.7])
    child_mesh.paint_uniform_color([0.1, 0.7, 0.1])

    frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.15)

    print("\nVista previa:")
    print("Gris = parent")
    print("Verde = child transformado")
    print("Cierra la ventana para terminar.\n")

    o3d.visualization.draw_geometries([parent_mesh, child_mesh, frame])


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--parent-mesh", required=True)
    parser.add_argument("--child-mesh", required=True)

    parser.add_argument("--parent-xyz", default="0 0 0")
    parser.add_argument("--parent-rpy", default="0 0 0")

    parser.add_argument("--child-xyz", default="0 0 0")
    parser.add_argument("--child-rpy", default="0 0 0")

    parser.add_argument("--features", type=int, default=3)
    parser.add_argument("--ring-points", type=int, default=8)
    parser.add_argument("--samples", type=int, default=120000)

    args = parser.parse_args()

    parent_xyz = parse_vec(args.parent_xyz)
    parent_rpy = parse_vec(args.parent_rpy)

    child_xyz = parse_vec(args.child_xyz)
    child_rpy = parse_vec(args.child_rpy)

    T_parent_visual = make_transform(parent_xyz, parent_rpy)
    T_child_visual = make_transform(child_xyz, child_rpy)

    parent_centers_raw = collect_hole_centers(
        mesh_path=args.parent_mesh,
        title="PARENT",
        features=args.features,
        min_points=args.ring_points,
        samples=args.samples
    )

    child_centers_raw = collect_hole_centers(
        mesh_path=args.child_mesh,
        title="CHILD",
        features=args.features,
        min_points=args.ring_points,
        samples=args.samples
    )

    parent_centers_link = transform_points(parent_centers_raw, T_parent_visual)
    child_centers_link = transform_points(child_centers_raw, T_child_visual)

    T_parent_child = best_fit_transform(child_centers_link, parent_centers_link)

    xyz = T_parent_child[:3, 3]
    roll, pitch, yaw = matrix_to_rpy(T_parent_child[:3, :3])

    print("\n====================================================")
    print("RESULTADO PARA PEGAR EN EL .XACRO")
    print("====================================================")
    print(
        f'<origin xyz="{xyz[0]:.6f} {xyz[1]:.6f} {xyz[2]:.6f}" '
        f'rpy="{roll:.6f} {pitch:.6f} {yaw:.6f}"/>'
    )
    print("====================================================\n")

    preview_result(
        args.parent_mesh,
        args.child_mesh,
        T_parent_visual,
        T_child_visual,
        T_parent_child
    )


if __name__ == "__main__":
    main()