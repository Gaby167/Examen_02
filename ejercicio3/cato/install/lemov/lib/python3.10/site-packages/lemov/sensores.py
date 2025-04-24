#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan

class SensorReaderNode(Node):
    def __init__(self):
        super().__init__('sensor_reader')
        # Suscripción única a /base_scan
        self.scan_sub = self.create_subscription(
            LaserScan,
            '/base_scan',
            self.scan_callback,
            10
        )

    def scan_callback(self, msg: LaserScan):
        # Lectura del segundo rayo (índice 1) y del último rayo
        try:
            sensor_one = msg.ranges[22]
            sensor_medio = msg.ranges[135]
            sensor_last = msg.ranges[225]
        except (IndexError, TypeError):
            self.get_logger().error('Error al leer los rangos del LaserScan')
            return
        if sensor_one <0.7:
            sensor_one = 0.0
        if sensor_medio <0.7:
            sensor_medio = 0.0
        if sensor_last <0.7:
            sensor_last = 0.0
        # Mostrar en pantalla solo los dos valores
        self.get_logger().info(
            f"Sensores -> Índice dere: {sensor_one:.2f} m |  indice front: {sensor_medio:.2f} Índice izq: {sensor_last:.2f} m"
        )


def main(args=None):
    rclpy.init(args=args)
    node = SensorReaderNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
