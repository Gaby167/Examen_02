#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import numpy as np
from sensor_msgs.msg import JointState
from builtin_interfaces.msg import Time

class IKPublisher(Node):
    def __init__(self):
        super().__init__('ik_rviz_node')
        self.publisher = self.create_publisher(JointState, 'joint_states', 10)
        self.timer = self.create_timer(1.0, self.solve_and_publish)
        self.get_logger().info("Nodo de IK conectado a RViz iniciado.")

    def solve_and_publish(self):
        try:
            x = float(input("Ingrese x objetivo: "))
            y = float(input("Ingrese y objetivo: "))

            # Parámetros
            l2, l3, l4 = 0.4, 0.3, 0.2
            L = l3 + l4
            r = np.sqrt(x**2 + y**2)
            D = (r**2 - l2**2 - L**2) / (2 * l2 * L)

            if np.abs(D) > 1:
                self.get_logger().error("Punto fuera del alcance.")
                return

            theta2 = np.arccos(D)
            theta1 = np.arctan2(y, x) - np.arctan2(L * np.sin(theta2), l2 + L * np.cos(theta2))
            theta3 = 0.0
            theta4 = 0 - (theta1 + theta2 + theta3)  # mantener orientación cero

            # Crear mensaje
            msg = JointState()
            msg.header.stamp = self.get_clock().now().to_msg()
            msg.name = ['joint1', 'joint2', 'joint3', 'joint4']
            msg.position = [theta1, theta2, theta3, theta4]

            # Publicar
            self.publisher.publish(msg)
            self.get_logger().info(f"Publicando posiciones: {np.degrees(theta1):.1f}, {np.degrees(theta2):.1f}, {np.degrees(theta3):.1f}, {np.degrees(theta4):.1f}")

        except Exception as e:
            self.get_logger().error(f"Error: {e}")

def main(args=None):
    rclpy.init(args=args)
    node = IKPublisher()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
