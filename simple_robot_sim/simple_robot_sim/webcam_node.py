import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image
from cv_bridge import CvBridge

import cv2


class WebcamNode(Node):
    def __init__(self):
        super().__init__('webcam_node')

        self.pub = self.create_publisher(Image, '/camera/image_raw', 10)

        self.bridge = CvBridge()

        self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
            self.get_logger().error('No se pudo abrir la cámara web')
            return

        self.timer = self.create_timer(0.033, self.publish_frame)  # aprox 30 Hz

        self.get_logger().info('Nodo webcam iniciado publicando en /camera/image_raw')

    def publish_frame(self):
        ret, frame = self.cap.read()

        if not ret:
            self.get_logger().warn('No se pudo leer frame de la cámara')
            return

        msg = self.bridge.cv2_to_imgmsg(frame, encoding='bgr8')
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'camera_link'

        self.pub.publish(msg)

    def destroy_node(self):
        if self.cap.isOpened():
            self.cap.release()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)

    node = WebcamNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
