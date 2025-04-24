#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist

class AvoidObstaclesNode(Node):
    def __init__(self):
        super().__init__('avoid_obstacles')
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.scan_sub = self.create_subscription(LaserScan, '/base_scan', self.scan_callback, 10)
        self.odom_sub = self.create_subscription(Odometry, '/odom', self.odom_callback, 10)
        self.timer = self.create_timer(0.1, self.move)

        # Variables de estado
        self.front = float('inf')
        self.left = float('inf')
        self.right = float('inf')
        self.actual_speed = 0.0  # velocidad real del robot
        self.trabado = False     # flag de colisión

    def scan_callback(self, msg):
        num = len(msg.ranges)

        # Distancia mínima en cada zona
        self.front = min(msg.ranges[num//2 - 10:num//2 + 10])   # frente
        self.left = min(msg.ranges[num//2 + 30:num//2 + 90])    # izquierda
        self.right = min(msg.ranges[num//2 - 90:num//2 - 30])   # derecha

    def odom_callback(self, msg):
        self.actual_speed = msg.twist.twist.linear.x

    def move(self):
        twist = Twist()

        # Distancia segura por zona
        safe_front = 1.0
        safe_side = 0.7

        # Detección de atascamiento: quiere avanzar pero no lo logra
        if self.front > safe_front and self.left > safe_side and self.right > safe_side:
            if self.actual_speed < 0.01:
                self.trabado = True
                self.get_logger().warn("🚧 ¡Robot atascado! Girando para liberarse...")
                twist.linear.x = 0.0
                twist.angular.z = 0.8
            else:
                self.trabado = False
                twist.linear.x = 0.25
                twist.angular.z = 0.0
        else:
            self.trabado = False
            twist.linear.x = 0.05
            if self.left > self.right:
                twist.angular.z = 0.6
                self.get_logger().info("↪️ Gira a la izquierda")
            else:
                twist.angular.z = -0.6
                self.get_logger().info("↩️ Gira a la derecha")

        self.cmd_pub.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = AvoidObstaclesNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()