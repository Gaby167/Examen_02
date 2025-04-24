#include <rclcpp/rclcpp.hpp>
#include <geometry_msgs/msg/pose.hpp>
#include <moveit/move_group_interface/move_group_interface.h>
#include <moveit/planning_scene_interface/planning_scene_interface.h>
#include <shape_msgs/msg/solid_primitive.hpp>
#include <iostream>

using moveit::planning_interface::MoveGroupInterface;
using moveit::planning_interface::PlanningSceneInterface;

void addObstacles(const std::shared_ptr<rclcpp::Node> &node, MoveGroupInterface &move_group) {
    PlanningSceneInterface planning_scene_interface;
    std::vector<moveit_msgs::msg::CollisionObject> collision_objects;

    // Caja 1
    moveit_msgs::msg::CollisionObject box1;
    box1.header.frame_id = move_group.getPlanningFrame();
    box1.id = "box1";

    shape_msgs::msg::SolidPrimitive primitive1;
    primitive1.type = primitive1.BOX;
    primitive1.dimensions = {0.3, 0.3, 0.3};

    geometry_msgs::msg::Pose pose1;
    pose1.orientation.w = 1.0;
    pose1.position.x = 0.5;
    pose1.position.y = 0.0;
    pose1.position.z = 0.15;

    box1.primitives.push_back(primitive1);
    box1.primitive_poses.push_back(pose1);
    box1.operation = box1.ADD;

    // Caja 2
    moveit_msgs::msg::CollisionObject box2;
    box2.header.frame_id = move_group.getPlanningFrame();
    box2.id = "box2";

    shape_msgs::msg::SolidPrimitive primitive2;
    primitive2.type = primitive2.BOX;
    primitive2.dimensions = {0.2, 0.2, 0.4};

    geometry_msgs::msg::Pose pose2;
    pose2.orientation.w = 1.0;
    pose2.position.x = 0.3;
    pose2.position.y = -0.4;
    pose2.position.z = 0.2;

    box2.primitives.push_back(primitive2);
    box2.primitive_poses.push_back(pose2);
    box2.operation = box2.ADD;

    collision_objects.push_back(box1);
    collision_objects.push_back(box2);
    planning_scene_interface.addCollisionObjects(collision_objects);

    RCLCPP_INFO(node->get_logger(), "Obstáculos añadidos al entorno.");
    rclcpp::sleep_for(std::chrono::seconds(2));
}

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = rclcpp::Node::make_shared("panda_ik_menu");
    rclcpp::executors::SingleThreadedExecutor executor;
    executor.add_node(node);

    MoveGroupInterface move_group(node, "panda_arm");

    move_group.setPlanningTime(15.0);
    move_group.setMaxVelocityScalingFactor(0.5);
    move_group.setMaxAccelerationScalingFactor(0.5);
    move_group.setPlannerId("RRTConnectkConfigDefault");

    addObstacles(node, move_group);

    while (rclcpp::ok()) {
        std::cout << "\n===== MENU =====\n"
                  << "1. Posición 1\n"
                  << "2. Posición 2\n"
                  << "3. Posición 3\n"
                  << "4. Ingresar coordenadas manualmente\n"
                  << "5. Salir\n> ";

        int opcion;
        std::cin >> opcion;

        geometry_msgs::msg::Pose target_pose;
        bool ejecutar_movimiento = true;

        switch (opcion) {
            case 1:
                target_pose.orientation.w = 1.0;
                target_pose.position.x = -0.58;
                target_pose.position.y = 0.2;
                target_pose.position.z = 0.5;
                break;

            case 2:
                target_pose.orientation.w = 0.7;
                target_pose.position.x = 0.4;
                target_pose.position.y = 0.4;
                target_pose.position.z = 0.2;
                break;

            case 3:
                target_pose.orientation.w = 1.0;
                target_pose.position.x = 0.3;
                target_pose.position.y = 0.2;
                target_pose.position.z = 0.5;
                break;

            case 4:
                std::cout << "X: "; std::cin >> target_pose.position.x;
                std::cout << "Y: "; std::cin >> target_pose.position.y;
                std::cout << "Z: "; std::cin >> target_pose.position.z;
                target_pose.orientation.w = 1.0;
                break;

            case 5:
                RCLCPP_INFO(node->get_logger(), "Saliendo...");
                rclcpp::shutdown();
                return 0;

            default:
                std::cout << "Opción inválida\n";
                ejecutar_movimiento = false;
                break;
        }

        if (ejecutar_movimiento) {
            move_group.setPoseTarget(target_pose);
            auto result = move_group.move();
            if (result != moveit::core::MoveItErrorCode::SUCCESS) {
                RCLCPP_WARN(node->get_logger(), "Falla");
            } else {
                RCLCPP_INFO(node->get_logger(), "Done");
            }
        }
    }

    rclcpp::shutdown();
    return 0;
}
