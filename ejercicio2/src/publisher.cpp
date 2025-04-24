#include <rclcpp/rclcpp.hpp>
#include <moveit/move_group_interface/move_group_interface.hpp>
#include <geometry_msgs/msg/pose.hpp>
#include <iostream>

using moveit::planning_interface::MoveGroupInterface;

void moverBrazo(MoveGroupInterface& move_group, double x, double y, double z, double w) {
    geometry_msgs::msg::Pose target_pose;
    target_pose.orientation.w = w;
    target_pose.position.x = x;
    target_pose.position.y = y;
    target_pose.position.z = z;

    move_group.setPoseTarget(target_pose);
    auto success = (move_group.move() == moveit::core::MoveItErrorCode::SUCCESS);

    if (!success) {
        std::cout << "No se pudo." << std::endl;
    } else {
        std::cout << "Hecho" << std::endl;
    }
}

int main(int argc, char** argv)
{
    rclcpp::init(argc, argv);
    auto node = rclcpp::Node::make_shared("publisher");
    rclcpp::executors::SingleThreadedExecutor executor;
    executor.add_node(node);

    MoveGroupInterface move_group(node, "panda_arm");
    move_group.setPlanningTime(15.0);
    move_group.setMaxVelocityScalingFactor(0.5);
    move_group.setMaxAccelerationScalingFactor(0.5);

    int opcion = 0;
    while (rclcpp::ok() && opcion != 5) {
        std::cout << "\n===== MENU =====" << std::endl;
        std::cout << "1. Posición 1" << std::endl;
        std::cout << "2. Posición 2" << std::endl;
        std::cout << "3. Posición 3" << std::endl;
        std::cout << "4. Ingresar coordenadas manualmente" << std::endl;
        std::cout << "5. Salir" << std::endl;
        std::cout << "> ";
        std::cin >> opcion;

        switch (opcion) {
            case 1:
                moverBrazo(move_group, -0.58, 0.2, 0.5, 1.0);
                break;
            case 2:
                moverBrazo(move_group, 0.9, 0.4, 0.1, 0.7);
                break;
            case 3:
                moverBrazo(move_group, 1.5, 1.1, 0.9, 1.5);
                break;
            case 4: {
                double x, y, z, w;
                std::cout << "Ingrese X: "; std::cin >> x;
                std::cout << "Ingrese Y: "; std::cin >> y;
                std::cout << "Ingrese Z: "; std::cin >> z;
                std::cout << "Ingrese W (orientación): "; std::cin >> w;
                moverBrazo(move_group, x, y, z, w);
                break;
            }
            case 5:
                std::cout << "Saliendo" << std::endl;
                break;
            default:
                std::cout << "Opción invalida\n";
                break;
        }
    }

    rclcpp::shutdown();
    return 0;
}
