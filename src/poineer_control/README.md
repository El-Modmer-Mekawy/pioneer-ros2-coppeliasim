# Pioneer 3-DX Teleoperation and Sensor Visualization (MTR 431 - Assignment 1)

## Overview
This ROS 2 package (`pioneer_control`) interfaces with CoppeliaSim to control a Pioneer 3-DX mobile robot via keyboard teleoperation (`/cmd_vel`) and visualizes its 16 ultrasonic proximity sensors in real-time using Matplotlib (`/ultrasonic_sensors`).

## Prerequisites
* **OS & ROS 2:** Ubuntu 22.04 (ROS 2 Humble) or Ubuntu 24.04 (ROS 2 Jazzy)
* **Simulator:** CoppeliaSim (with `simROS2` plugin enabled)
* **Python Libraries:** `matplotlib` (`pip install matplotlib` or `sudo apt install python3-matplotlib`)

## Build Instructions
1. Place the `pioneer_control` package inside your ROS 2 workspace `src` folder:
   ```bash
   cd ~/ros2_ws
   colcon build --packages-select pioneer_control
   source install/setup.bash

   