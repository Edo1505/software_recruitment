from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='reseq',
            executable='temperature_sensor',
            name='sensor_node',
            output='screen'
        ),
        Node(
            package='reseq',
            executable='temperature_logger',
            name='logger_node',
            output='screen'
        ),
    ])