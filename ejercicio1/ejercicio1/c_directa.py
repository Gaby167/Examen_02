import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from sympy import symbols, Matrix, cos, sin, pi, simplify, N

class FKSolver(Node):
    def __init__(self):
        super().__init__('fk_solver')
        self.publisher = self.create_publisher(JointState, 'joint_states', 10)
        self.get_logger().info("Nodo FK con publicación a RViz iniciado.")
        self.calculate_and_publish()

    def dh(self, theta, d, a, alpha):
        return Matrix([
            [cos(theta), -sin(theta)*cos(alpha), sin(theta)*sin(alpha), a*cos(theta)],
            [sin(theta), cos(theta)*cos(alpha), -cos(theta)*sin(alpha), a*sin(theta)],
            [0, sin(alpha), cos(alpha), d],
            [0, 0, 0, 1]
        ])

    def calculate_and_publish(self):
        q1, q2, q3, q4 = symbols('q1 q2 q3 q4')

        # Cinemática simbólica
        A1 = self.dh(q1, 0.6, 0.0, pi/2)
        A2 = self.dh(q2, 0.0, 0.4, 0.0)
        A3 = self.dh(q3, 0.0, 0.3, 0.0)
        A4 = self.dh(q4, 0.0, 0.2, 0.0)

        T04 = simplify(A1 * A2 * A3 * A4)
        self.get_logger().info("T_04 simbólica:")
        print(T04)

        # Pedir valores numéricos
        q_vals_deg = []
        for i in range(1, 5):
            val = float(input(f"Ingrese q{i} en grados: "))
            q_vals_deg.append(val)

        q_vals_rad = [v * (pi / 180) for v in q_vals_deg]
        subs = dict(zip([q1, q2, q3, q4], q_vals_rad))

        T_num = T04.evalf(subs=subs)
        position = T_num[:3, 3]
        self.get_logger().info("Posición final del efector (x, y, z):")
        print(f"x = {N(position[0]):.4f}")
        print(f"y = {N(position[1]):.4f}")
        print(f"z = {N(position[2]):.4f}")

        # Publicar al joint_states
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = ['joint1', 'joint2', 'joint3', 'joint4']
        msg.position = [float(v) for v in map(N, q_vals_rad)]

        self.publisher.publish(msg)
        self.get_logger().info("✅ Posiciones publicadas en /joint_states")

def main(args=None):
    rclpy.init(args=args)
    node = FKSolver()
    rclpy.spin_once(node, timeout_sec=1.0)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
