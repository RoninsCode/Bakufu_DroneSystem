# Installation Guide

## Requirements
- Ubuntu 20.04 LTS
- ROS Noetic
- PX4-Autopilot
- Gazebo
- Python ML Environment

## Setup Steps
I'll provide you with the installation commands for each component, along with brief explanations:

## 1. Ubuntu 20.04 LTS
This needs to be installed first as the base operating system. Download from ubuntu.com and follow installation instructions.

## 2. ROS Noetic Installation

# Setup sources.list
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'

# Set up keys
sudo apt install curl
curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo apt-key add -

# Update package list
sudo apt update

# Install ROS Noetic (full desktop version)
sudo apt install ros-noetic-desktop-full

# Initialize rosdep
sudo rosdep init
rosdep update

# Environment setup
echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc
source ~/.bashrc

# Install dependencies for building packages
sudo apt install python3-rosdep python3-rosinstall python3-rosinstall-generator python3-wstool build-essential


## 3. PX4-Autopilot Installation

# Install git and required dependencies
sudo apt install git python3-pip

# Clone PX4-Autopilot
git clone https://github.com/PX4/PX4-Autopilot.git
cd PX4-Autopilot

# Run the ubuntu.sh script with no interactive prompts
bash ./Tools/setup/ubuntu.sh --no-sim-tools --no-nuttx

# Build SITL (Software In The Loop)
make px4_sitl


## 4. Gazebo Installation

# Gazebo should already be installed with ROS full desktop
# But ensure you have the latest version
sudo apt update
sudo apt upgrade gazebo

# Install Gazebo ROS packages
sudo apt install ros-noetic-gazebo-ros-pkgs ros-noetic-gazebo-ros-control


## 5. MAVROS Installation

# Install MAVROS and GeographicLib dependencies
sudo apt install ros-noetic-mavros ros-noetic-mavros-extras

# Install GeographicLib datasets
wget https://raw.githubusercontent.com/mavlink/mavros/master/mavros/scripts/install_geographiclib_datasets.sh
sudo bash ./install_geographiclib_datasets.sh


## Additional Dependencies

# Install additional dependencies that might be needed
sudo apt install python3-pip python3-numpy python3-yaml
pip3 install --user pyros-genmsg setuptools


## Post-Installation Verification

# Test PX4 SITL with Gazebo
cd PX4-Autopilot
make px4_sitl gazebo

# In another terminal, test MAVROS
roslaunch mavros px4.launch fcu_url:="udp://:14540@127.0.0.1:14557"


Important Notes:
1. Execute commands in order
2. Some commands might take significant time to complete
3. Ensure you have good internet connection
4. You might need to restart your computer after installation
5. If you encounter errors, check system requirements and dependencies

