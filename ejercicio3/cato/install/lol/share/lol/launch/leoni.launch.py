#!/usr/bin/env python3
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    # Localiza los directorios de los paquetes
    stage_share = get_package_share_directory('stage_ros2')
    nav_share = get_package_share_directory('navigation_tb3')

    return LaunchDescription([
        # 1) Stage simulator
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(stage_share, 'launch', 'stage.launch.py')
            ),
            launch_arguments={
                'world': 'mapa',
                'enforce_prefixes': 'false',
                'one_tf_tree': 'true'
            }.items()
        ),

        # 2) SLAM / mapeo
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(nav_share, 'launch', 'mapping.launch.py')
            )
        ),

        # 3) RViz con configuración predefinida
        Node(
            package='rviz2', executable='rviz2',
            arguments=['-d', os.path.join(nav_share, 'config', 'mapping.rviz')],
            output='screen'
        ),

        # 4) Nodo de movimiento 'lemov move'
        Node(
            package='lemov', executable='movisen',
            output='screen'
        ),
    ])
