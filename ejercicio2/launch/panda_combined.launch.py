from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import os

from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    panda_moveit_config_path = get_package_share_directory('moveit_resources_panda_moveit_config')
    
    demo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(panda_moveit_config_path, 'launch', 'demo.launch.py')
        )
    )

    publisher2_node = ExecuteProcess(
        cmd=['ros2', 'run', 'robot_description', 'publisher2'],
        output='screen'
    )

    return LaunchDescription([
        demo_launch,
        publisher2_node
    ])
