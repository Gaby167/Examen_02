#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sympy import symbols, Matrix, sin, cos, pi, simplify

class JacobianCalculator(Node):
    def __init__(self):
        super().__init__('jacobiana_solver')
        self.get_logger().info("Calculando Jacobiana simbólica...")

        # Variables
        q1, q2, q3, q4 = symbols('q1 q2 q3 q4')
        l1, l2, l3, l4 = 0.6, 0.4, 0.3, 0.2

        def dh(theta, d, a, alpha):
            return Matrix([
                [cos(theta), -sin(theta)*cos(alpha), sin(theta)*sin(alpha), a*cos(theta)],
                [sin(theta), cos(theta)*cos(alpha), -cos(theta)*sin(alpha), a*sin(theta)],
                [0, sin(alpha), cos(alpha), d],
                [0, 0, 0, 1]
            ])

        # DH matrices
        A1 = dh(q1, l1, 0, pi/2)
        A2 = dh(q2, 0, l2, 0)
        A3 = dh(q3, 0, l3, 0)
        A4 = dh(q4, 0, l4, 0)

        T01 = simplify(A1)
        T02 = simplify(T01 * A2)
        T03 = simplify(T02 * A3)
        T04 = simplify(T03 * A4)

        # Puntos de interés
        o0 = Matrix([0, 0, 0])
        o1 = T01[:3, 3]
        o2 = T02[:3, 3]
        o3 = T03[:3, 3]
        o4 = T04[:3, 3]  # posición del efector

        z0 = Matrix([0, 0, 1])
        z1 = T01[:3, 2]
        z2 = T02[:3, 2]
        z3 = T03[:3, 2]

        # Jacobiana lineal (3x4)
        Jv = Matrix.hstack(
            z0.cross(o4 - o0),
            z1.cross(o4 - o1),
            z2.cross(o4 - o2),
            z3.cross(o4 - o3)
        )

        # Jacobiana angular (3x4)
        Jw = Matrix.hstack(z0, z1, z2, z3)

        # Jacobiana total (6x4)
        J = simplify(Matrix.vstack(Jv, Jw))

        print("\n📌 Jacobiana simbólica (6x4):")
        print(J)

def main(args=None):
    rclpy.init(args=args)
    node = JacobianCalculator()
    rclpy.spin_once(node, timeout_sec=1.0)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
