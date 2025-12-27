from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    return LaunchDescription([

        # --- RTAB-Map SLAM node (MAP OWNER) ---
        Node(
            package='rtabmap_slam',
            executable='rtabmap',
            name='rtabmap',
            output='screen',
            parameters=[{
                # Frames
                'frame_id': 'base_link',
                'odom_frame_id': 'camera_init',   # FAST-LIO odom
                'map_frame_id': 'map',

                # Inputs
                'subscribe_scan_cloud': True,
                'subscribe_depth': False,
                'subscribe_rgb': False,
                'approx_sync': False,

                # TF handling
                'wait_for_transform': 0.8,
                'publish_tf': True,

                # Graph SLAM
                'Mem/IncrementalMemory': 'true',
                'Mem/InitWMWithAllNodes': 'true',

                # Loop closure
                'RGBD/ProximityBySpace': 'true',
                'RGBD/AngularUpdate': '0.05',
                'RGBD/LinearUpdate': '0.05',

                # ICP (use FAST-LIO-quality cloud)
                'Reg/Strategy': '1',
                'Icp/PointToPlane': 'true',
                'Icp/VoxelSize': '0.1',
                'Icp/MaxCorrespondenceDistance': '1.0',
                'Icp/Iterations': '10',
                'Icp/Epsilon': '0.001',
                'Icp/OutlierRatio': '0.7',

                # Occupancy grid (OPTIONAL but useful for Nav2)
                'RGBD/CreateOccupancyGrid': 'true',
                'Grid/FromDepth': 'false',
                'Grid/3D': 'true',
                'Grid/RangeMax': '10.0',
                'Grid/CellSize': '0.05',
                'Grid/MinGroundHeight': '0.00',
                'Grid/MaxGroundHeight': '0.02',
                'Grid/RayTracing': 'true',

                'use_sim_time': True,
            }],
            remappings=[
                ('scan_cloud', '/cloud_registered_body')
            ],
            arguments=['-d', '--ros-args', '--log-level', 'Error']  # delete previous db
        ),

        # --- Optional: RTAB-Map visualization ---
        Node(
            package='rtabmap_viz',
            executable='rtabmap_viz',
            name='rtabmap_viz',
            output='screen',
            parameters=[{
                'frame_id': 'base_link',
                'odom_frame_id': 'camera_init',
                'subscribe_scan_cloud': True,
                'use_sim_time': True,
            }],
            remappings=[
                ('scan_cloud', '/cloud_registered_body')
            ]
        ),
    ])
