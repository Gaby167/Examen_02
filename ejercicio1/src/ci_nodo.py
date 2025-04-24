#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import numpy as np

class IKSolver(Node):
    def __init__(self):
        super().__init__('ik_solver')
        self.get_logger().info("Nodo de Cinemática Inversa iniciado.")
        self.solve()

    def solve(self):
        try:
            x = float(input("Ingrese la coordenada x objetivo: "))
            y = float(input("Ingrese la coordenada y objetivo: "))

            # Longitudes de eslabones
            l2 = 0.4
            l3 = 0.3
            l4 = 0.2
            L = l3 + l4  # eslabón combinado

            r = np.sqrt(x**2 + y**2)
            D = (r**2 - l2**2 - L**2) / (2 * l2 * L)

            if np.abs(D) > 1:
                self.get_logger().error("⚠️ Posición fuera del alcance.")
                return

            # Calcular ángulos (solución tipo codo abajo)
            theta2 = np.arccos(D)
            theta1 = np.arctan2(y, x) - np.arctan2(L * np.sin(theta2), l2 + L * np.cos(theta2))

            # Suponemos orientación deseada nula para este ejemplo
            theta3 = 0.0

            # Mostrar resultados en grados
            self.get_logger().info("Ángulos obtenidos:")
            print(f"q1 (base)   = {np.degrees(theta1):.2f}°")
            print(f"q2 (codo)   = {np.degrees(theta2):.2f}°")
            print(f"q3 (muñeca) = {np.degrees(theta3):.2f}°")

        except Exception as e:
            self.get_logger().error(f"Error: {e}")

def main(args=None):
    rclpy.init(args=args)
    node = IKSolver()
    rclpy.spin_once(node, timeout_sec=1.0)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
