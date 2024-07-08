#include <ros/ros.h>
#include <sensor_msgs/LaserScan.h>
#include <sensor_msgs/PointCloud.h>
#include <sensor_msgs/PointCloud2.h>
#include <sensor_msgs/Imu.h>
#include <sensor_msgs/Image.h> // Include for sensor_msgs/Image
#include <laser_geometry/laser_geometry.h>

class LaserToCloudConverter {
    ros::NodeHandle nh_;
    laser_geometry::LaserProjection projector_;
    ros::Subscriber laser_sub_;
    ros::Publisher cloud_pub_;
    ros::Subscriber imu_sub_; // IMU subscriber
    ros::Publisher imu_pub_; // IMU publisher
    ros::Subscriber image_sub_; // Image subscriber
    ros::Publisher image_pub_; // Image publisher

public:
    LaserToCloudConverter() {
        laser_sub_ = nh_.subscribe<sensor_msgs::LaserScan>("amr/scan", 1, &LaserToCloudConverter::scanCallback, this);
        cloud_pub_ = nh_.advertise<sensor_msgs::PointCloud>("linefeature_tracker/linefeature", 1, false);
        imu_sub_ = nh_.subscribe<sensor_msgs::Imu>("imu", 1, &LaserToCloudConverter::imuCallback, this); // Subscribe to /imu
        imu_pub_ = nh_.advertise<sensor_msgs::Imu>("imu0", 1, false); // Publish to /imu0
        image_sub_ = nh_.subscribe<sensor_msgs::Image>("camera/rgb/image_raw", 1, &LaserToCloudConverter::imageCallback, this); // Subscribe to /camera/rgb/image_raw
        image_pub_ = nh_.advertise<sensor_msgs::Image>("cam0/image_raw", 1, false); // Publish to /cam0/image_raw
    }

    void scanCallback(const sensor_msgs::LaserScan::ConstPtr& scan) {
        sensor_msgs::PointCloud cloud;
        projector_.projectLaser(*scan, cloud);
        cloud_pub_.publish(cloud);
    }

    void imuCallback(const sensor_msgs::Imu::ConstPtr& imu) {
        imu_pub_.publish(imu);
    }

    void imageCallback(const sensor_msgs::Image::ConstPtr& image) {
        image_pub_.publish(image);
    }
};

int main(int argc, char** argv) {
    ros::init(argc, argv, "laser_to_cloud_converter");
    LaserToCloudConverter converter;
    ros::spin();
    return 0;
}