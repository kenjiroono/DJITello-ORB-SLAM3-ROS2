# tello-ros2
- This is modified version of [tello-ros2](https://github.com/tentone/tello-ros2)
- [DJI Tello](https://www.ryzerobotics.com/tello) driver for ROS 2 based on [DJITelloPy](https://github.com/damiafuentes/DJITelloPy) that uses the [official SDK](https://github.com/dji-sdk/Tello-Python) for the drone.
- Ii is recommended to update the Tello firmware to the latest version available 
- Project workspace is divided into sub-workspaces that contain different logic.
  - `tello` package is the main package, includes access to the drone information, camera image and  control.
  - `tello_msg` package defines custom messages to access specific Tello data.
    - Defines the `TelloStatus`, `TelloID` and `TelloWifiConfig` messages 
  - `tello_control` package is a sample control package that displays the drone image and provides keyboard control.
    - T used for takeoff, L to land the drone, F to flip forward, E for emergency stop, WASD and arrows to control the drone movement.
  - `tello_control_gamepad` package allows tello drone to be manually controlled by the connected Xbox controller(USB).

## Environment:
- Ubuntu 22.04
- ROS2 Humble 
