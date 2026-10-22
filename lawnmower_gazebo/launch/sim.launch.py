import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    pkg_desc = get_package_share_directory('lawnmower_description')
    pkg_gazebo = get_package_share_directory('lawnmower_gazebo')
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')

    # 1. Process URDF/Xacro
    xacro_file = os.path.join(pkg_desc, 'urdf', 'lawnmower.urdf.xacro')
    robot_description_config = xacro.process_file(xacro_file)
    robot_desc = {'robot_description': robot_description_config.toxml(), 'use_sim_time': True}

    # 2. World File Path
    world_file = os.path.join(pkg_gazebo, 'worlds', 'lawn.world')

    # 3. Robot State Publisher
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot_desc]
    )

    # 4. Launch Gazebo with Custom Lawn World
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gazebo.launch.py')
        ),
        launch_arguments={'world': world_file}.items()
    )

    # 5. Spawn Robot in Gazebo
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', 'robot_description', '-entity', 'autonomous_lawnmower', '-z', '0.15'],
        output='screen'
    )

    return LaunchDescription([
        node_robot_state_publisher,
        gazebo,
        spawn_entity,
    ])