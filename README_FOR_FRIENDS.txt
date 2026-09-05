Synaids Multi-AMR Warehouse Simulation
======================================

REQUIREMENTS
------------
Ubuntu 24.04
ROS 2 Jazzy
Gazebo Sim 8 / Gazebo Harmonic

PROJECT LOCATION
----------------
After extracting, place the folder in:

~/synaids_amr


RUN THE WAREHOUSE
-----------------
Open Terminal 1:

source /opt/ros/jazzy/setup.bash
export LIBGL_ALWAYS_SOFTWARE=1
gz sim ~/synaids_amr/worlds/warehouse_realistic.sdf


RUN THE ROS BRIDGE
------------------
Open Terminal 2:

source /opt/ros/jazzy/setup.bash

ros2 run ros_gz_bridge parameter_bridge \
/R1/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist \
/R1/odom@nav_msgs/msg/Odometry@gz.msgs.Odometry \
/R1/scan@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan \
/R2/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist \
/R2/odom@nav_msgs/msg/Odometry@gz.msgs.Odometry \
/R2/scan@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan \
/R3/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist \
/R3/odom@nav_msgs/msg/Odometry@gz.msgs.Odometry \
/R3/scan@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan


BUILD THE FLEET COORDINATOR
---------------------------
Open Terminal 3:

source /opt/ros/jazzy/setup.bash
cd ~/synaids_amr/ros2_ws

colcon build --packages-select fleet_coordinator

source install/setup.bash


RUN THE FLEET COORDINATOR
-------------------------
In Terminal 3:

source /opt/ros/jazzy/setup.bash
source ~/synaids_amr/ros2_ws/install/setup.bash

ros2 run fleet_coordinator coordinator


MAIN WORLD
----------
~/synaids_amr/worlds/warehouse_realistic.sdf

The warehouse contains:
- 3 AMRs: R1, R2, R3
- Central intersection/conflict zone
- Storage racks
- Inventory/pallets
- Pickup areas
- Drop-off areas
- Charging station
- Restricted area
- Safety barriers/bollards
- Warehouse traffic markings


IMPORTANT
---------
Do NOT copy the old build/install/log folders from another computer.
Run colcon build on the new computer after extracting the project.
