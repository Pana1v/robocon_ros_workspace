cmake_minimum_required(VERSION 3.0.2)
project(laser_to_cloud_converter)

find_package(catkin REQUIRED COMPONENTS
    roscpp
    sensor_msgs
    pcl_ros
    laser_geometry
)

catkin_package(
    CATKIN_DEPENDS roscpp sensor_msgs pcl_ros laser_geometry
)

include_directories(
    ${catkin_INCLUDE_DIRS}
)

add_executable(${PROJECT_NAME}_node src/main.cpp)

target_link_libraries(${PROJECT_NAME}_node
    ${catkin_LIBRARIES}
)