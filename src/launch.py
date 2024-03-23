
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    nodes = [
        # Tello driver node
        Node(
            package='tello',
            executable='tello',
            output='screen',
            namespace='/',
            name='tello',
            parameters=[
                {'connect_timeout': 10.0},
                {'tello_ip': '192.168.10.1'},
                {'tf_base': 'map'},
                {'tf_drone': 'drone'}
            ],
            remappings=[
                ('/image_raw', '/camera')
            ],
            respawn=True
        ),

        # # Tello control node
        # Node(
        #     package='tello_control',
        #     executable='tello_control',
        #     namespace='/',
        #     name='control',
        #     output='screen',
        #     respawn=False
        # ),

        #RQT topic debug tool
        Node(
            package='rqt_gui',
            executable='rqt_gui',
            output='screen',
            namespace='/',
            name='rqt',
            respawn=False
        ),

        # RViz data visualization tool
        Node(
            package='rviz2',
            executable='rviz2',
            output='screen',
            namespace='/',
            name='rviz2',
            respawn=True,
            arguments=['-d', '/home/tentone/Git/tello-slam/workspace/src/rviz.rviz']
        ),

        # Static TF publisher
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            namespace='/',
            name='tf',
            arguments=['0', '0', '0', '0', '0', '0', '1', 'map', 'drone'],
            respawn=True
        ),


        # Tello gamepad control node
        Node(
            package='tello_control_gamepad',
            executable='tello_control_gamepad',
            namespace='/',
            name='tello_control_gamepad',
            output='screen',
            respawn=False
        ),

        # ORB-SLAM node
        Node(
            package='ros2_orb_slam3',
            executable='mono_node_cpp',
            output='screen',
            namespace='/',
            name='ros2_orb_slam3',
            respawn=True,
            # remappings=[
            #     ('/camera', '/image_raw')
            # ],
            # arguments=['~/Git/tello-slam/libs/ORB_SLAM2/Vocabulary/ORBvoc.txt', '~/Git/tello-slam/workspace/src/orbslam2/config.yaml']
        ),

        # ORB-SLAM driver node
        # Node(
        #     package='ros2_orb_slam3',
        #     executable='mono_tello_driver_node',
        #     namespace='/',
        #     name='mono_tello_driver_node',
        #     output='screen',
        #     respawn=True
        # ),

        # Camera calibration node
        # Node(
        #     package='camera_calibration',
        #     executable='cameracalibrator',
        #     output='screen',
        #     respawn=True,
        #     namespace='/',
        #     name='calibration',
        #     arguments=['--size', '7x9', '--square', '0.20'],
        #     parameters=[
        #         {'image': '/image_raw'},
        #         {'camera': '/camera_info'}
        #     ]
        # )
    ]

    return LaunchDescription(nodes)