import rclpy
from rclpy.node import Node

from sensor_msgs.msg import PointCloud2, PointField
from std_msgs.msg import Header

import cv2
import struct
import numpy as np


class WebcamPointCloud(Node):
    def __init__(self):
        super().__init__('webcam_pointcloud')

        self.pub = self.create_publisher(PointCloud2, '/camera/points', 10)

        self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
            self.get_logger().error('No se pudo abrir la cámara')
            return

        self.timer = self.create_timer(0.1, self.publish_cloud)

        self.get_logger().info('Publicando nube de puntos falsa en /camera/points')

    def publish_cloud(self):
        ret, frame = self.cap.read()

        if not ret:
            return

        frame = cv2.resize(frame, (160, 120))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        height, width = gray.shape

        points = []

        fx = 120.0
        fy = 120.0
        cx = width / 2.0
        cy = height / 2.0

        for v in range(0, height, 2):
            for u in range(0, width, 2):
                brightness = gray[v, u] / 255.0

                z = 0.5 + brightness * 2.5

                x = (u - cx) * z / fx
                y = (v - cy) * z / fy

                b, g, r = frame[v, u]

                rgb = struct.unpack('I', struct.pack('BBBB', b, g, r, 255))[0]

                points.append([x, y, z, rgb])

        msg = PointCloud2()
        msg.header = Header()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'camera_link'

        msg.height = 1
        msg.width = len(points)

        msg.fields = [
            PointField(name='x', offset=0, datatype=PointField.FLOAT32, count=1),
            PointField(name='y', offset=4, datatype=PointField.FLOAT32, count=1),
            PointField(name='z', offset=8, datatype=PointField.FLOAT32, count=1),
            PointField(name='rgb', offset=12, datatype=PointField.UINT32, count=1),
        ]

        msg.is_bigendian = False
        msg.point_step = 16
        msg.row_step = msg.point_step * len(points)
        msg.is_dense = True

        buffer = []

        for p in points:
            buffer.append(struct.pack('fffI', p[0], p[1], p[2], p[3]))

        msg.data = b''.join(buffer)

        self.pub.publish(msg)

    def destroy_node(self):
        if self.cap.isOpened():
            self.cap.release()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)

    node = WebcamPointCloud()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
