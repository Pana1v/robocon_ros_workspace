#!/bin/bash

# Check if script is run as root, if not, re-run with sudo
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root. Re-running with sudo."
   sudo "$0" "$@"
   exit $?
fi

# Set up your sources list
echo "Setting up sources list for ROS Noetic..."
sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-noetic.list'

# Set up your keys
echo "Setting up keys for ROS Noetic..."
apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654

# Update package index
echo "Updating package index..."
apt update

# Install ROS Noetic Desktop Full
echo "Installing ROS Noetic Desktop Full..."
apt install -y ros-noetic-desktop-full

# Initialize rosdep
echo "Initializing rosdep..."
rosdep init
rosdep update

# Set up the ROS environment
echo "Setting up ROS environment..."
echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc
source ~/.bashrc

# Install additional ROS tools
echo "Installing additional ROS tools..."
apt install -y python3-rosinstall python3-rosinstall-generator python3-wstool build-essential

# Set up the workspace
WORKSPACE_DIR=~/robocon_ros_workspace/src
echo "Setting up the workspace at $WORKSPACE_DIR..."
mkdir -p $WORKSPACE_DIR
cd $WORKSPACE_DIR

# Download and run the provided installation script
echo "Downloading and running the ros_install_noetic.sh script..."
wget -c https://raw.githubusercontent.com/qboticslabs/ros_install_noetic/master/ros_install_noetic.sh
chmod +x ./ros_install_noetic.sh
./ros_install_noetic.sh

echo "ROS Noetic installation and workspace setup complete."