import rclpy                          # Librería cliente de ROS 2 para Python
from rclpy.node import Node           # Clase base para crear nodos
from std_msgs.msg import String

class VelocityPublisher(Node):
    def __init__(self):
        super().__init__('velocity_publisher')  

        self.publisher_ = self.create_publisher(
            Int32, 
            'velocidad',            
            10    
        )

        timer_period = 0.5           
        self.timer = self.create_timer(timer_period, self.timer_callback)

        self.v_x = 0               

    def timer_callback(self):
        msg = Int32()              
        msg.data = self.v_x  
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publicando v_x: {msg.data}')
        self.v_x += 1               


def main(args=None):
    rclpy.init(args=args)            # Inicializa la comunicación con ROS 2
    publisher = VelocityPublisher()
    rclpy.spin(publisher)            # Mantiene el nodo activo, ejecutando callbacks
    publisher.destroy_node()         # Limpieza explícita 
    rclpy.shutdown()


if __name__ == '__main__':
    main()