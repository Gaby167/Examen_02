from sympy import symbols, Matrix, cos, sin, pi, simplify

# Variables simbólicas
q1, q2, q3, q4 = symbols('q1 q2 q3 q4')
l1, l2, l3, l4 = 0.6, 0.4, 0.3, 0.2

# Tabla DH (θ, d, a, α)
dh_params = [
    [q1, l1, 0,   pi/2],
    [q2, 0,  l2,  0],
    [q3, 0,  l3,  0],
    [q4, 0,  l4,  0],
]

# Función para construir matriz DH
def dh(theta, d, a, alpha):
    return Matrix([
        [cos(theta), -sin(theta)*cos(alpha),  sin(theta)*sin(alpha), a*cos(theta)],
        [sin(theta),  cos(theta)*cos(alpha), -cos(theta)*sin(alpha), a*sin(theta)],
        [0,           sin(alpha),             cos(alpha),            d],
        [0,           0,                      0,                     1]
    ])

# Multiplicación secuencial de matrices
T = Matrix.eye(4)
for i, (theta, d, a, alpha) in enumerate(dh_params):
    A = dh(theta, d, a, alpha)
    print(f"\nA{i+1} = ")
    print(simplify(A))
    T = T * A

print("\n📌 Matriz T04 final:")
print(simplify(T))

def main():
    print("Matriz DH")

if __name__ == '__main__':
    main()